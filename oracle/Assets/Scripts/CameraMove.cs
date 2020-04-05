using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

public class CameraMove : MonoBehaviour
{
    [SerializeField]
    private float speed = 0.5f;

    [SerializeField]
    private UIManager ui = null;

    private Vector3 oldPos;
    private Vector3 panOrigin;
    private bool dragging;

    void Start()
    {
        Assert.IsNotNull(ui);
        dragging = false;
    }

    void LateUpdate()
    {
        if(!ui.isUISelected())
        {
            var click = Input.GetAxis("Fire1");
            if(click != 0 && !dragging)
            {
                oldPos = transform.position;
                panOrigin = Camera.main.ScreenToViewportPoint(Input.mousePosition);
            }

            dragging = click != 0;

            if(dragging)
            {
                var pos = Camera.main.ScreenToViewportPoint(Input.mousePosition) - panOrigin;
                var mappedValue = ui.RemapZoomValue(.2f, 1);
                transform.position = oldPos + -pos * speed * mappedValue;
            }
        }
    }

    void Update()
    {
        var horizontal = Input.GetAxis("Horizontal");
        var vertical = Input.GetAxis("Vertical");
        var mappedValue = ui.RemapZoomValue(.2f, 1);
        transform.Translate(new Vector3(speed * mappedValue * Time.deltaTime * horizontal, 0, 0));
        transform.Translate(new Vector3(0, speed * mappedValue * Time.deltaTime * vertical, 0));
    }
}
