using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class Noise
{
    public enum NormalizeMode {Local, Global};

    // create a function to create a noisemap
    public static float[,] GenerateNoiseMap(int mapWidth, int mapHeight, int seed, float scale, int octaves, float persistance, float lacunarity, Vector2 offset, NormalizeMode normalizeMode) {
        // create an empty noisemap 
        float[,] noiseMap = new float[mapWidth, mapHeight];

        // randomize octaves
        System.Random prng = new System.Random(seed); // create a random number generator
        float maxGlobalHeight = 0;
        float amplitude = 1;
        float frequency = 1;

        Vector2[] octaveOffsets = new Vector2[octaves]; // array for offsets of each vector
        for (int i = 0; i < octaves; i++) {
            float offsetX = prng.Next(-100000, 100000) + offset.x; // randomize offset
            float offsetY = prng.Next(-100000, 100000) - offset.y;
            octaveOffsets[i] = new Vector2(offsetX, offsetY); // set values in array to randomized values

            maxGlobalHeight += amplitude;
            amplitude *= persistance;
        }

        // octaves: layers of noisemaps
        // persistance: controls amplitudes of octaves -- higher octaves = lower amplitudes (less impact)
        // lacunarity: controls frequency of octaves -- higher octaves = higher lacunarity (more detail)

        float maxNoise = float.MinValue;
        float minNoise = float.MaxValue;

        float halfWidth = mapWidth / 2f;
        float halfHeight = mapHeight / 2f;

        // copy perlin noise map to empty noisemap
        for (int y = 0; y < mapHeight; y++) {
            for (int x = 0; x < mapWidth; x++) {

                amplitude = 1;
                frequency = 1;
                float noiseHeight = 0; // culmunative amplitude (of octaves)

                // for every octave
                for (int i = 0; i < octaves; i++) {
                    // x and y values (updated with scale and frequency)
                    float sampleX = (x - halfWidth + octaveOffsets[i].x) * scale * frequency;
                    float sampleY = (y - halfHeight + octaveOffsets[i].y) * scale * frequency;
                    
                    // generates perlin values
                    float perlinValue = Mathf.PerlinNoise(sampleX, sampleY) * 2 - 1; // value * 2 - 1 allows for negative values
                    noiseHeight += perlinValue * amplitude;

                    // applies changes in amplitude and frequency
                    amplitude *= persistance;
                    frequency *= lacunarity;
                }

                // update min and max
                if (noiseHeight > maxNoise) {
                    maxNoise = noiseHeight;
                }
                if (noiseHeight < minNoise) {
                    minNoise = noiseHeight;
                }

                // update noisemap
                noiseMap[x, y] = noiseHeight;
            }
        }

        // normalize noisemap (update values to between 0 and 1)
        for (int y = 0; y < mapHeight; y++) {
            for (int x = 0; x < mapWidth; x++) {
                if (normalizeMode == NormalizeMode.Local) {
                    noiseMap[x, y] = Mathf.InverseLerp(minNoise, maxNoise, noiseMap[x, y]);
                } else {
                    float normalizedHeight = (noiseMap[x, y] + 1) / maxGlobalHeight;
                    noiseMap[x, y] = Mathf.Clamp(normalizedHeight, 0, int.MaxValue);
                }
                
            }
        }
        return noiseMap;
    }
}

