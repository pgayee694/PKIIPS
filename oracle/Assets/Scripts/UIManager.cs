using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.Assertions;

/// <summary>
/// This script is used to manage the UI.
/// </summary>
[RequireComponent(typeof(EventSystem))]
public class UIManager : MonoBehaviour
{
    /// <summary>
    /// The UI slider for zooming. Needs to be set in the inspector window.
    /// </summary>
    [SerializeField]
    private Slider zoomSlider = null;

    /// <summary>
    /// Public attribute to the current zoom value.
    /// </summary>
    public float ZoomValue
    {
        get { return zoomSlider.value; }
        set { zoomSlider.value = value; }
    }

    /// <summary>
    /// The speed at which to zoom in and out. Can be set in the inspector window.
    /// </summary>
    [SerializeField]
    private float zoomSpeed = 1f;

    /// <summary>
    /// Public attribute to the current zoom speed;
    /// </summary>
    public float ZoomSpeed
    {
        get { return zoomSpeed; }
        set { zoomSpeed = value; }
    }

    /// <summary>
    /// Public attribute to the current zoom slider.
    /// </summary>
    public Slider ZoomSlider
    {
        get { return zoomSlider; }
    }

    /// <summary>
    /// The button to go up a floor. Needs to be set in the inspector window.
    /// </summary>
    [SerializeField]
    private Button upFloorButton = null;

    /// <summary>
    /// Public attribute to the up floor button.
    /// </summary>
    public Button UpFloorButton
    {
        get { return upFloorButton; }
    }

    /// <summary>
    /// The button to go down a floor. Needs to be set in the inspector window.
    /// </summary>
    [SerializeField]
    private Button downFloorButton = null;

    /// <summary>
    /// Public attribute to the down floor button.
    /// </summary>
    public Button DownFloorButton
    {
        get { return downFloorButton; }
    }

    /// <summary>
    /// The text that displays the current floor. Needs to be set in the inspector window.
    /// </summary>
    [SerializeField]
    private Text floorText = null;

    /// <summary>
    /// Public attribute to the floor text.
    /// </summary>
    public Text FloorText
    {
        get { return floorText; }
    }

    /// <summary>
    /// The current floor number.
    /// </summary>
    private int floor;

    /// <summary>
    /// Public attribute to the current floor number.
    /// Setting a value to this attribute changes the floor.
    /// </summary>
    public int Floor
    {
        get { return floor; }
        set
        {
            if(value < 1 || value > floors.Count)
            {
                return;
            }

            floor = value;
            floorText.text = Floor.ToString();
            if(currentFloor != null)
            {
                Destroy(currentFloor);
            }

            currentFloor = Instantiate<Floor>(floors[Floor - 1], new Vector3(0, 0, 0), Quaternion.identity);
        }
    }

    /// <summary>
    /// Public attribute to the current zoom value.
    /// </summary>
    [SerializeField]
    private Canvas canvas = null;

    /// <summary>
    /// Public attribute to the current zoom value.
    /// </summary>
    [SerializeField]
    private List<Floor> floors = new List<Floor>();

    /// <summary>
    /// The currently instantiated <code>Floor</code> game object.
    /// <see cref="Floor"/>
    /// </summary>
    private Floor currentFloor = null;

    /// <summary>
    /// The event system attached to this game object.
    /// </summary>
    private EventSystem eventSystem;

    /// <summary>
    /// Called in the first frame. Sets up variables.
    /// </summary>
    void Start()
    {
        Assert.IsNotNull(canvas);
        Assert.IsNotNull(ZoomSlider);
        Assert.IsNotNull(UpFloorButton);
        Assert.IsNotNull(DownFloorButton);
        Assert.IsNotNull(FloorText);
        eventSystem = GetComponent<EventSystem>();
        Assert.IsNotNull(eventSystem);
        Floor = 1;
        UpdateCameraZoom();
    }

    /// <summary>
    /// Called every frame.
    /// </summary>
    void Update()
    {
        var scroll = Input.GetAxis("Mouse ScrollWheel");
        ZoomValue -= scroll * ZoomSpeed;
    }

    /// <summary>
    /// Gets the currently selected UI element.
    /// </summary>
    /// <returns>
    /// Returns the currrently selected game object.
    /// </returns>
    public GameObject CurrentSelectedObject()
    {
        return eventSystem.currentSelectedGameObject;
    }

    /// <summary>
    /// Checks if the user is currently clicking a UI element.
    /// </summary>
    /// <returns>
    /// True if the user is clicking a UI element, false otherwise.
    /// </returns>
    public bool isClickingUI()
    {
        return eventSystem.IsPointerOverGameObject();
    }

    /// <summary>
    /// Checks if a UI element has the current focus.
    /// </summary>
    /// <returns>
    /// True if the user is selecting a UI element, false otherwise.
    /// </returns>
    public bool isUISelected()
    {
        return isZoomSliderSelected() ||
               isUpFloorButtonSelected() ||
               isDownFloorButtonSelected();
    }

    /// <summary>
    /// Checks if the zoom slider has the current focus.
    /// </summary>
    /// <returns>
    /// True if the user is selecting the zoom slider, false otherwise.
    /// </returns>
    public bool isZoomSliderSelected()
    {
        return CurrentSelectedObject() == ZoomSlider.gameObject;
    }

    /// <summary>
    /// Checks if the up floor button has the current focus.
    /// </summary>
    /// <returns>
    /// True if the user is selecting the up floor button, false otherwise.
    /// </returns>
    public bool isUpFloorButtonSelected()
    {
        return CurrentSelectedObject() == UpFloorButton.gameObject;
    }

    /// <summary>
    /// Checks if the down floor button has the current focus.
    /// </summary>
    /// <returns>
    /// True if the user is selecting the down floor button, false otherwise.
    /// </returns>
    public bool isDownFloorButtonSelected()
    {
        return CurrentSelectedObject() == DownFloorButton.gameObject;
    }

    /// <summary>
    /// Updates the main camera's zoom to the current zoom value.
    /// </summary>
    public void UpdateCameraZoom()
    {
        Camera.main.orthographicSize = ZoomValue;
    }

    /// <summary>
    /// Gets the current canvas game object.
    /// </summary>
    /// <returns>
    /// Canvas game object.
    /// </returns>
    public Canvas getCanvas()
    {
        return canvas;
    }

    /// <summary>
    /// Increment the floor number by one.
    /// </summary>
    public void incrementFloor()
    {
        Floor += 1;
    }

    /// <summary>
    /// Decrements the floor number by one.
    /// </summary>
    public void decrementFloor()
    {
        Floor -= 1;
    }

    /// <summary>
    /// Maps the zoom slider's range to the given range.
    /// </summary>
    /// <returns>
    /// The remapped value.
    /// </returns>
    public float RemapZoomValue(float from, float to)
    {
        return Remap(ZoomValue, ZoomSlider.minValue, ZoomSlider.maxValue, from, to);
    }

    /// <summary>
    /// Maps a value from one range to another.
    /// </summary>
    /// <returns>
    /// The remapped value.
    /// </returns>
    private float Remap(float value, float from1, float to1, float from2, float to2)
    {
        return (value - from1) / (to1 - from1) * (to2 - from2) + from2;
    }
}
