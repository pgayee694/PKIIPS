using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

/// <summary>
/// Script mainly used to be put onto a camera to control its movement.
/// </summary>
public class CameraMove : MonoBehaviour
{
    /// <summary>
    /// Speed at which the camera will move around.
    /// </summary>
    [SerializeField]
    private float speed = 0.5f;

    /// <summary>
    /// A <code>UIManager</code> to be used to check if the UI is being
    /// clicked on to avoid moving the screen while dragging. Also used
    /// to remap the speed value when zoomed in. 
    /// </summary>
    [SerializeField]
    private UIManager ui = null;

    /// <summary>
    /// A record of the original camera position before click and dragging.
    /// </summary>
    private Vector3 oldPos;

    /// <summary>
    /// A record of the original mouse position before click and dragging.
    /// </summary>
    private Vector3 panOrigin;

    /// <summary>
    /// Whether the user is currently dragging on the screen.
    /// </summary>
    private bool dragging;

    /// <summary>
    /// Called in its first frame. Sets default values.
    /// </summary>
    void Start()
    {
        Assert.IsNotNull(ui);
        dragging = false;
    }

    /// <summary>
    /// Called after the <code>Update</code> method.
    /// If the UI is not being used, this will allow the user
    /// to click and drag the mouse to move the camera.
    /// <see cref="Update"/>
    /// </summary>
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

    /// <summary>
    /// Called every frame. This allows the user to move the camera
    /// with the keyboard.
    /// </summary>
    void Update()
    {
        var horizontal = Input.GetAxis("Horizontal");
        var vertical = Input.GetAxis("Vertical");
        var mappedValue = ui.RemapZoomValue(.2f, 1);
        transform.Translate(new Vector3(speed * mappedValue * Time.deltaTime * horizontal, 0, 0));
        transform.Translate(new Vector3(0, speed * mappedValue * Time.deltaTime * vertical, 0));
    }
}
