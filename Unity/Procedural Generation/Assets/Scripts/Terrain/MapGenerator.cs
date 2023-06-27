using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading;

public class MapGenerator : MonoBehaviour
{    
    // variables
    public const int chunkSize = 241;
    [Range (0,6)]
    public int detailLevel;
    public float noiseScale;

    public float heightMultiplier;
    public AnimationCurve heightCurve;

    public int octaves;
    [Range (0,1)]
    public float persistance;
    public float lacunarity;

    public Vector2 offset;
    public int seed;
    public bool autoUpdate;

    public enum DrawMode {NoiseMap, ColourMap, Mesh};
    public DrawMode drawMode;
    public Noise.NormalizeMode normalizeMode;

    public TerrainType[] regions;

    Queue<MapThreadInfo<MapData>> mapDataThreadInfoQueue = new Queue<MapThreadInfo<MapData>>();
    Queue<MapThreadInfo<MeshData>> meshDataThreadInfoQueue = new Queue<MapThreadInfo<MeshData>>();

    // generate noisemap and colourmap
    private MapData GenerateMapData (Vector2 centre) {
        // create a new noisemap
        float[,] noiseMap = Noise.GenerateNoiseMap(chunkSize, chunkSize, seed, noiseScale, octaves, persistance, lacunarity, centre + offset, normalizeMode);

        // create an empty colourmap
        Color[] colourMap = new Color[chunkSize * chunkSize];

        for (int y = 0; y < chunkSize; y++) {
            for (int x = 0; x < chunkSize; x++) {
                // change colourmap based on noisemap and regions
                float height = noiseMap[x, y];
                for (int i = 0; i < regions.Length; i++) {
                    if (height >= regions[i].height) {
                        colourMap[y * chunkSize + x] = regions[i].colour;
                    } else {
                        break;
                    }
                }
            }
        }
        return new MapData(noiseMap, colourMap);
    }
//////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// THREADING STUFF: CONFUSING /////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////
    public void RequestMapData(Vector2 centre, Action<MapData> callback) {
        ThreadStart threadStart = delegate {
            MapDataThread(centre, callback);
        };

        new Thread(threadStart).Start();
    }

    private void MapDataThread(Vector2 centre, Action<MapData> callback) {
        MapData mapData = GenerateMapData(centre);
        lock (mapDataThreadInfoQueue) { // when one thread executes code, another thread cannot execute
            mapDataThreadInfoQueue.Enqueue(new MapThreadInfo<MapData>(callback, mapData));
        }
    }

    public void RequestMeshData(MapData mapData, int lod, Action<MeshData> callback) {
        ThreadStart threadStart = delegate {
            MeshDataThread(mapData, lod, callback);
        };

        new Thread(threadStart).Start();
    }

    private void MeshDataThread(MapData mapData, int lod, Action<MeshData> callback) {
        MeshData meshData = MeshGenerator.GenerateTerrainMesh(mapData.heightMap, heightMultiplier, heightCurve, lod);
        lock (meshDataThreadInfoQueue) { // when one thread executes code, another thread cannot execute
            meshDataThreadInfoQueue.Enqueue(new MapThreadInfo<MeshData>(callback, meshData));
        }
    }

    void Update() {
        if (mapDataThreadInfoQueue.Count > 0) {
            for (int i = 0; i < mapDataThreadInfoQueue.Count; i++) {
                MapThreadInfo<MapData> threadInfo = mapDataThreadInfoQueue.Dequeue(); // gets next item in queue
                threadInfo.callback(threadInfo.parameter);
            }
        }

        if (meshDataThreadInfoQueue.Count > 0) {
            for (int i = 0; i < meshDataThreadInfoQueue.Count; i++) {
                MapThreadInfo<MeshData> threadInfo = meshDataThreadInfoQueue.Dequeue();
                threadInfo.callback(threadInfo.parameter);
            }
        }
    }
//////////////////////////////////////////////////////////////////////////////////////////////

    public void MapEditor () {
        MapData mapData = GenerateMapData(Vector2.zero);

        // create a colourmap (MapDisplay > DisplayMap)
        MapDisplay display = FindObjectOfType <MapDisplay>(); // find the plane object

        // display the noisemap/colourmap
        if (drawMode == DrawMode.ColourMap) {
            display.DrawTexture(TextureGenerator.TextureFromColourMap(mapData.colourMap, chunkSize, chunkSize));
        }
        else if (drawMode == DrawMode.NoiseMap) {
            display.DrawTexture(TextureGenerator.TextureFromHeightMap(mapData.heightMap));
        }
        else if (drawMode == DrawMode.Mesh) {
            display.DrawMesh(MeshGenerator.GenerateTerrainMesh(mapData.heightMap, heightMultiplier, heightCurve, detailLevel), TextureGenerator.TextureFromColourMap(mapData.colourMap, chunkSize, chunkSize));
        }
    }

    private void OnValidate() {
        if (octaves < 1) {
            octaves = 1;
        }
        if (lacunarity < 1) {
            lacunarity = 1;
        }
    }

    struct MapThreadInfo<T> {
        public readonly Action<T> callback;
        public readonly T parameter;

        public MapThreadInfo(Action<T> callback, T parameter) {
            this.callback = callback;
            this.parameter = parameter;
        }
    }
}

[System.Serializable]
public struct TerrainType {
    public string name;
    public float height;
    public Color colour;
}

public struct MapData {
    public readonly float[,] heightMap;
    public readonly Color[] colourMap;

    public MapData(float[,] heightMap, Color[] colourMap) {
        this.heightMap = heightMap;
        this.colourMap = colourMap;
    }
}