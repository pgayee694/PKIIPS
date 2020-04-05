using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.Assertions;

[RequireComponent(typeof(EventSystem))]
public class UIManager : MonoBehaviour
{
    [SerializeField]
    private Slider zoomSlider = null;

    public float ZoomValue
    {
        get { return zoomSlider.value; }
        set { zoomSlider.value = value; }
    }

    [SerializeField]
    private float zoomSpeed = 1f;

    public float ZoomSpeed
    {
        get { return zoomSpeed; }
        set { zoomSpeed = value; }
    }

    public Slider ZoomSlider
    {
        get { return zoomSlider; }
    }

    [SerializeField]
    private Button upFloorButton = null;

    public Button UpFloorButton
    {
        get { return upFloorButton; }
    }

    [SerializeField]
    private Button downFloorButton = null;

    public Button DownFloorButton
    {
        get { return downFloorButton; }
    }

    [SerializeField]
    private Text floorText = null;

    public Text FloorText
    {
        get { return floorText; }
    }

    private int floor;

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

    [SerializeField]
    private Canvas canvas = null;

    [SerializeField]
    private List<Floor> floors = new List<Floor>();

    private Floor currentFloor = null;
    private EventSystem eventSystem;

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
    }

    void Update()
    {
        var scroll = Input.GetAxis("Mouse ScrollWheel");
        ZoomValue -= scroll * ZoomSpeed;
    }

    public GameObject CurrentSelectedObject()
    {
        return eventSystem.currentSelectedGameObject;
    }

    public bool isClickingUI()
    {
        return eventSystem.IsPointerOverGameObject();
    }

    public bool isUISelected()
    {
        return isZoomSliderSelected() ||
               isUpFloorButtonSelected() ||
               isDownFloorButtonSelected();
    }

    public bool isZoomSliderSelected()
    {
        return CurrentSelectedObject() == ZoomSlider.gameObject;
    }

    public bool isUpFloorButtonSelected()
    {
        return CurrentSelectedObject() == UpFloorButton.gameObject;
    }

    public bool isDownFloorButtonSelected()
    {
        return CurrentSelectedObject() == DownFloorButton.gameObject;
    }

    public void UpdateCameraZoom()
    {
        Camera.main.orthographicSize = ZoomValue;
    }

    public Canvas getCanvas()
    {
        return canvas;
    }

    public void incrementFloor()
    {
        Floor += 1;
    }

    public void decrementFloor()
    {
        Floor -= 1;
    }

    public float RemapZoomValue(float from, float to)
    {
        return Remap(ZoomValue, ZoomSlider.minValue, ZoomSlider.maxValue, from, to);
    }

    private float Remap(float value, float from1, float to1, float from2, float to2)
    {
        return (value - from1) / (to1 - from1) * (to2 - from2) + from2;
    }
}
