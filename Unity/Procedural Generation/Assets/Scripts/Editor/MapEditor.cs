using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

// used to add button to GUI
[CustomEditor (typeof (MapGenerator))]
public class MapEditor : Editor
{
    public override void OnInspectorGUI() {
        MapGenerator mapGen = (MapGenerator)target;

        if (DrawDefaultInspector()) {
            if (mapGen.autoUpdate) {
                mapGen.MapEditor();
            }
        }

        if (GUILayout.Button("Generate")) {
            mapGen.MapEditor();
        }
    }
}
