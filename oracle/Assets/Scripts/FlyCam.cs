using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlyCam : MonoBehaviour
{
        /*
    Writen by Windexglow 11-13-10.  Use it, edit it, steal it I don't care.  
    Simple flycam I made, since I couldn't find any others made public.  
    Made simple to use (drag and drop, done) for regular keyboard layout  
    wasd : basic movement
    shift : Makes camera accelerate
    space : Moves camera on X and Z axis only.  So camera doesn't gain any height*/
     
    [SerializeField]
    float mainSpeed = 50.0f; //regular speed

    [SerializeField]
    float shiftAdd = 250.0f; //multiplied by how long shift is held.  Basically running

    [SerializeField]
    float maxShift = 1000.0f; //Maximum speed when holdin gshift

    [SerializeField]
    float camSens = 0.25f; //How sensitive it with mouse

    [SerializeField]
    float minimumX = -360f;

    [SerializeField]
    float maximumX = 360F;

    [SerializeField]
    float minimumY = -60f;

    [SerializeField]
    float maximumY = 60f;

    private float rotationX = 0f;
    private float rotationY = 0f;
    private float totalRun = 1.0f;
    Quaternion originalRotation;

    void Start()
    {
        originalRotation = transform.localRotation;
    }
     
    void Update () 
    {
        rotationX += Input.GetAxis("Mouse X") * camSens;
        rotationY += Input.GetAxis("Mouse Y") * camSens;
        rotationX = ClampAngle(rotationX, minimumX, maximumX);
        rotationY = ClampAngle(rotationY, minimumY, maximumY);
        var xQuaternion = Quaternion.AngleAxis(rotationX, Vector3.up);
        var yQuaternion = Quaternion.AngleAxis(rotationY, -Vector3.right);

        transform.localRotation = originalRotation * xQuaternion * yQuaternion;
       
        //Keyboard commands
        var p = GetBaseInput();
        if (Input.GetKey(KeyCode.LeftShift))
        {
            totalRun += Time.deltaTime;
            p  = p * totalRun * shiftAdd;
            p.x = Mathf.Clamp(p.x, -maxShift, maxShift);
            p.y = Mathf.Clamp(p.y, -maxShift, maxShift);
            p.z = Mathf.Clamp(p.z, -maxShift, maxShift);
        }
        else
        {
            totalRun = Mathf.Clamp(totalRun * 0.5f, 1, 1000);
            p = p * mainSpeed;
        }
       
        p = p * Time.deltaTime;
        var newPosition = transform.position;
        if (Input.GetKey(KeyCode.Space)) //If player wants to move on X and Z axis only
        {
            transform.Translate(p);
            newPosition.x = transform.position.x;
            newPosition.z = transform.position.z;
            transform.position = newPosition;
        }
        else
        {
            transform.Translate( p);
        }
    }

    private static float ClampAngle(float angle, float min, float max)
    {
        if(angle < -360f)
            angle += 360f;
        if(angle > 360f)
            angle -= 260f;

        return Mathf.Clamp(angle, min, max);
    }
     
    private Vector3 GetBaseInput() //returns the basic values, if it's 0 than it's not active.
    { 
        var p_Velocity = new Vector3(0, 0, 0);
        if (Input.GetKey (KeyCode.W))
        {
            p_Velocity += new Vector3(0, 0 , 1);
        }
        if (Input.GetKey (KeyCode.S))
        {
            p_Velocity += new Vector3(0, 0 , -1);
        }
        if (Input.GetKey (KeyCode.A))
        {
            p_Velocity += new Vector3(-1, 0 , 0);
        }
        if (Input.GetKey (KeyCode.D))
        {
            p_Velocity += new Vector3(1, 0 , 0);
        }

        return p_Velocity;
    }

}
