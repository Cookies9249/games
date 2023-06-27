using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseMovement : MonoBehaviour
{
 
    public float mouseSensitivity = 800f;
    public Transform cameraTransform;
 
    float xRotation = 0f;
    float YRotation = 0f;
 
    void Start()
    {
      // Move cursor to middle and make it invisible
      Cursor.lockState = CursorLockMode.Locked;
    }
 
    void Update()
    {
       float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
       float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;
 
       // rotation around x axis (up and down), applied to camera only
       xRotation -= mouseY;
       // prevent over-rotate (like in real life)
       xRotation = Mathf.Clamp(xRotation, -90f, 90f);
       cameraTransform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
 
       // rotation around y axis (left and right), applied to player
       YRotation += mouseX;
       transform.localRotation = Quaternion.Euler(0f, YRotation, 0f);
    }
}

/*
Some extra notes:
- Instantiate(reference): copy a new mob
- OnCollisionEnter2D: Called with collision
- static: one instance of a variable exists for a class (easier to call from other scripts)

Events and Delegates: Used to called functions between scripts

public class Sender : MonoBehaviour {

  public delegate void PlayerDied (parameters);   // delegate: what is actually subscribed to (structure of events)
  public static event PlayerDied playerDiedInfo;  // the event (which can be detected by other scripts)

  void Start () {
    Invoke("ExecuteEvent", 5f);                   // calls ExecuteEvent function after 5 s
  }

  void ExecuteEvent () {
    if (playerDiedInfo != null) {
      playerDiedInfo(parameters);
    }
  }

}

public class Reciever : MonoBehaviour {

  void OnEnable () {
    Sender.playerDiedInfo += PlayerDiedListener;  // subscribes PlayerDiedListener function to the playerDiedInfo event
    //                                            // PlayerDiedListener is called when playerDiedInfo event is detected
  }

  void OnDisable () {
    Sender.playerDiedInfo -= PlayerDiedListener;  // unsubscribes
  }

  void PlayerDiedListener (parameters) {          // must have the same parameters as the delegate
    print("event detected");
  }

}


*/