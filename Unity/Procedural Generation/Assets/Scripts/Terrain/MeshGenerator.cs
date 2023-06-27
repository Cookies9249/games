using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class MeshGenerator
{
    public static MeshData GenerateTerrainMesh(float[,] noiseMap, float heightMultiplier, AnimationCurve _heightCurve, int detailLevel) {
        AnimationCurve heightCurve = new AnimationCurve(_heightCurve.keys);

        int width = noiseMap.GetLength(0);
        int height = noiseMap.GetLength(1);
        float topLeftX = (width - 1) / -2f;
        float topLeftZ = (height - 1) / 2f; 

        // detail increment is used to change detail of mesh
        int detailIncrement = (detailLevel == 0) ? 1 : detailLevel * 2;
        int verticesPerLine = (width - 1) / detailIncrement + 1;

        MeshData meshData = new MeshData(verticesPerLine, verticesPerLine);
        int vertexIndex = 0;

        for (int y = 0; y < height; y += detailIncrement) {
            for (int x = 0; x < width; x += detailIncrement) {
                // add verticies
                meshData.vertices[vertexIndex] = new Vector3(topLeftX + x, heightCurve.Evaluate(noiseMap[x, y]) * heightMultiplier, topLeftZ - y);

                // add uvs
                meshData.uvs[vertexIndex] = new Vector2(x / (float)width, y/ (float)height);

                // for every vertex, add two triangles
                if (x < width - 1 && y < height - 1) {
                    meshData.AddTriangle (vertexIndex, vertexIndex + verticesPerLine + 1, vertexIndex + verticesPerLine);
					meshData.AddTriangle (vertexIndex + verticesPerLine + 1, vertexIndex, vertexIndex + 1);
                }

                vertexIndex++;
            }
        }
        return meshData;
    }
}

public class MeshData {
    public Vector3[] vertices;
    public int[] triangles;
    public Vector2[] uvs;

    int triangleIndex;

    public MeshData(int meshWidth, int meshHeight) { // create meshdata constructor (__init__)
        vertices = new Vector3[meshWidth * meshHeight];
        uvs = new Vector2[meshWidth * meshHeight];
        triangles = new int[(meshWidth - 1) * (meshHeight - 1) * 6];
    }

    public void AddTriangle(int a, int b, int c) {
        triangles[triangleIndex] = a;
        triangles[triangleIndex+1] = b;
        triangles[triangleIndex+2] = c;
        triangleIndex += 3;
    }

    public Mesh CreateMesh() {
        Mesh mesh = new Mesh();
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.uv = uvs;
        mesh.RecalculateNormals();
        return mesh;
    }
}

