using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChunkLoader : MonoBehaviour
{
    const float scale = 10f;

    const float thresholdForUpdate = 25f;
    const float sqrThresholdForUpdate = thresholdForUpdate * thresholdForUpdate;

    public LODInfo[] detailLevels;
    public static float maxViewDistance;

    public Transform viewer;
    public Material mapMaterial;

    // pos: actual pos, coord: pos relative to chunk size
    public static Vector2 viewerPos;
    Vector2 viewerPosOld;
    static MapGenerator mapGenerator;
    int chunkSize;
    int visibleChunks;

    // dictionary of position and chunks
    Dictionary<Vector2, TerrainChunk> terrainChunkDict = new Dictionary<Vector2, TerrainChunk>();
    static List<TerrainChunk> terrainChunksLastUpdate = new List<TerrainChunk>();

    void Start() {
        mapGenerator = FindObjectOfType<MapGenerator>();

        maxViewDistance = detailLevels[detailLevels.Length - 1].visibleDistanceThreshold;
        chunkSize = MapGenerator.chunkSize - 1;
        visibleChunks = Mathf.RoundToInt(maxViewDistance / chunkSize);

        UpdateVisibleChunks();
    }

    // update visible chunks every frame
    void Update() {
        viewerPos = new Vector2(viewer.position.x, viewer.position.z) / scale;

        if ((viewerPosOld - viewerPos).sqrMagnitude > sqrThresholdForUpdate) {
            viewerPosOld = viewerPos;
            UpdateVisibleChunks();
        }
    }

    void UpdateVisibleChunks() {
        int currentChunkCoordX = Mathf.RoundToInt(viewerPos.x / chunkSize);
        int currentChunkCoordY = Mathf.RoundToInt(viewerPos.y / chunkSize);

        for (int i = 0; i < terrainChunksLastUpdate.Count; i++) {
            terrainChunksLastUpdate[i].SetVisible(false);
        }
        terrainChunksLastUpdate.Clear();


        for (int y = -visibleChunks; y <= visibleChunks; y++) {
            for (int x = -visibleChunks; x <= visibleChunks; x++) {
                Vector2 viewedChunkCoord = new Vector2(currentChunkCoordX + x, currentChunkCoordY + y);

                // checks if chunk is currently visible
                if (terrainChunkDict.ContainsKey(viewedChunkCoord)) {
                    terrainChunkDict[viewedChunkCoord].UpdateChunk();
                }
                else {
                    terrainChunkDict.Add(viewedChunkCoord, new TerrainChunk(viewedChunkCoord, chunkSize, detailLevels, transform, mapMaterial));
                }
            }
        }
    }

    public class TerrainChunk {
        GameObject meshObject;
        Vector2 pos;
        Bounds bounds;          // bounds: used to determine smallest distance from viewer to chunk

        MeshRenderer meshRenderer;
        MeshFilter meshFilter;
        MeshCollider meshCollider;

        LODInfo[] detailLevels;
        LODMesh[] lodMeshes;

        MapData mapData;
        bool mapDataReceived;
        int previousLODIndex = -1;

        public TerrainChunk(Vector2 coord, int size, LODInfo[] detailLevels, Transform parent, Material material) {
            this.detailLevels = detailLevels;

            pos = coord * size;
            bounds = new Bounds(pos, Vector2.one * size);
            Vector3 posV3 = new Vector3(pos.x, 0, pos.y);

            // set components of gameObject 
            meshObject = new GameObject("Terrain Chunk");
            meshRenderer = meshObject.AddComponent<MeshRenderer>();
            meshFilter = meshObject.AddComponent<MeshFilter>();
            meshCollider = meshObject.AddComponent<MeshCollider>();
            meshRenderer.material = material;

            meshObject.transform.position = posV3 * scale;
            meshObject.transform.parent = parent;
            meshObject.transform.localScale = Vector3.one * scale;
            SetVisible(false);

            lodMeshes = new LODMesh[detailLevels.Length];
            for (int i = 0; i < detailLevels.Length; i++) {
                lodMeshes[i] = new LODMesh(detailLevels[i].lod, UpdateChunk);
            }

            ////////// THREADING //////////
            mapGenerator.RequestMapData(pos, OnMapDataRecieved);
        }

        ////////// THREADING //////////
        void OnMapDataRecieved(MapData mapData) {
            this.mapData = mapData;
            mapDataReceived = true;

            Texture2D texture = TextureGenerator.TextureFromColourMap(mapData.colourMap, MapGenerator.chunkSize, MapGenerator.chunkSize);
            meshRenderer.material.mainTexture = texture;

            UpdateChunk();
        }

        // void OnMeshDataRecieved(MeshData meshData) {
        //     // print("mesh");
        //     // meshFilter.mesh = meshData.CreateMesh();
        // }

        // if the chunk is within distance, set visible
        public void UpdateChunk() {
            if (mapDataReceived) {
                float distanceToChunk = Mathf.Sqrt(bounds.SqrDistance(viewerPos));
                bool visible = distanceToChunk <= maxViewDistance;

                if (visible) {
                    int lodIndex = 0;
                    for (int i = 0; i < detailLevels.Length - 1; i++) {
                        if (distanceToChunk > detailLevels[i].visibleDistanceThreshold) {
                            lodIndex = i+1;
                        } else {
                            break;
                        }
                    }
                    if (lodIndex != previousLODIndex) {
                        LODMesh lodMesh = lodMeshes[lodIndex];
                        if (lodMesh.hasMesh) {
                            previousLODIndex = lodIndex;
                            meshFilter.mesh = lodMesh.mesh;
                            meshCollider.sharedMesh = lodMesh.mesh;
                        }
                        else if (!lodMesh.hasRequested) {
                            lodMesh.RequestMesh(mapData);
                        }
                    }

                    terrainChunksLastUpdate.Add(this);
                }
                SetVisible(visible);
            }
        }

        public void SetVisible(bool visible) {
            meshObject.SetActive(visible);
        }

        public bool isVisible() {
            return meshObject.activeSelf;
        }
    }

    class LODMesh {
        public Mesh mesh;
        public bool hasRequested;
        public bool hasMesh;
        int lod;
        System.Action updateCallback;

        public LODMesh(int lod, System.Action updateCallback) {
            this.lod = lod;
            this.updateCallback = updateCallback;
        }

        void OnMeshDataRecieved(MeshData meshData) {
            mesh = meshData.CreateMesh();
            hasMesh = true;

            updateCallback();
        }

        public void RequestMesh(MapData mapData) {
            hasRequested = true;
            mapGenerator.RequestMeshData(mapData, lod, OnMeshDataRecieved);
        }
    }

    [System.Serializable]
    public struct LODInfo {
        public int lod;
        public float visibleDistanceThreshold;
    }
}
