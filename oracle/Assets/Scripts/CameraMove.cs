using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMove : MonoBehaviour
{

    [SerializeField]
    private float speed = 0.5f;

    [SerializeField]
    private float zoom = 1f;

    [SerializeField]
    private float minZoom = 1f;

    [SerializeField]
    private float maxZoom = 10f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        var horizontal = Input.GetAxis("Horizontal");
        var vertical = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(speed * Time.deltaTime * horizontal, 0, 0));
        transform.Translate(new Vector3(0, speed * Time.deltaTime * vertical, 0));
        
        var scroll = Input.GetAxis("Mouse ScrollWheel");
        var newZoom = Camera.main.orthographicSize - scroll * zoom;
        if(newZoom > minZoom & newZoom < maxZoom)
        {
            Camera.main.orthographicSize = newZoom;
        }
    }
}
