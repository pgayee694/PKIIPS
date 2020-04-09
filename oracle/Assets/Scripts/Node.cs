using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

/// <summary>
/// Script used to model a "node" in our graph model.
/// Every node has a set of attributes.
/// </summary>
public class Node : MonoBehaviour
{
    /// <summary>
    /// The name of the people count attribute.
    /// </summary>
    public const string PeopleCountAttribute = "People Count";

    /// <summary>
    /// The name of the id attribute.
    /// </summary>
    public const string IdAttribute = "Room";

    /// <summary>
    /// The number of people in this node.
    /// </summary>
    private int peopleCount;

    /// <summary>
    /// An ID for this node.
    /// </summary>
    private int id;

    /// <summary>
    /// Public attribute for the <code>peopleCount</code> member.
    /// Updates the UI entry when this value gets sets.
    /// <see cref="peopleCount"/>
    /// </summary>
    public int PeopleCount
    {
        get { return peopleCount; }
        set
        {
            peopleCount = value;
            updateEntry(PeopleCountAttribute, peopleCount);
        }
    }

    /// <summary>
    /// Public attribute for the <code>id</code> member.
    /// Updates the UI entry when this value gets sets.
    /// <see cref="id"/>
    /// </summary>
    public int Id
    {
        get { return id; }
        set
        {
            id = value;
            updateEntry(IdAttribute, id);
        }
    }

    /// <summary>
    /// A <code>StatisticsBox</code> game object that can be used as
    /// a template to instantiate.
    /// <see cref="StatisticsBox"/>
    /// </summary>
    [SerializeField]
    private StatisticsBox statisticsTemplate = null;

    /// <summary>
    /// An offset of where the statistics box shows up relative
    /// to the node in the X coordinate.
    /// </summary>
    [SerializeField]
    private float statisticsPositionOffsetX = 0;

    /// <summary>
    /// An offset of where the statistics box shows up relative
    /// to the node in the Y coordinate.
    /// </summary>
    [SerializeField]
    private float statisticsPositionOffsetY = 0;

    /// <summary>
    /// The current game's <code>UIManager</code>. This is used to
    /// add the <code>StatisticsBox</code> UI to the game.
    /// <see cref="UIManager"/>
    /// <see cref="StatisticsBox"/>
    /// </summary>
    private UIManager ui;

    /// <summary>
    /// The currently instantiaed <code>StatisticsBox</code>.
    /// </summary>
    private StatisticsBox statistics = null;
    
    /// <summary>
    /// Called on the first frame. Sets up certain variables.
    /// </summary>
    void Start()
    {
        ui = GameObject.Find("EventSystem").GetComponent<UIManager>();
        Assert.IsNotNull(statisticsTemplate);
        Assert.IsNotNull(ui);
        PeopleCount = 0;
        Id = 0;
    }

    /// <summary>
    /// Called every frame.
    /// </summary>
    void Update()
    {
        updateStatisticsPosition();
    }

    /// <summary>
    /// The currently instantiated <code>StatisticsBox</code>.
    /// </summary>
    void OnMouseUp()
    {
        if(statistics == null)
        {
            statistics = Instantiate<StatisticsBox>(statisticsTemplate);
            statistics.transform.SetParent(ui.getCanvas().gameObject.transform);
            updateEntry(PeopleCountAttribute, PeopleCount);
            updateEntry(IdAttribute, Id);
            updateStatisticsPosition();
        }
        else
        {
            Destroy(statistics.gameObject);
        }
    }

    /// <summary>
    /// Called when this game object is destroyed.
    /// Will also destroy its corresponding statistics box.
    /// </summary>
    void OnDestroy()
    {
        if(statistics != null)
        {
            Destroy(statistics.gameObject);
        }

        Destroy(gameObject);
    }

    /// <summary>
    /// Updates an entry in the statistics box, if one exists.
    /// </summary>
    public void updateEntry<T>(string attributeName, T attribute)
    {
        if(statistics != null)
        {
            statistics.addEntry(attributeName, attribute);
        }
    }

    /// <summary>
    /// Moves the statistics box's position to the node, rather than just being stuck in
    /// the UI screen space.
    /// </summary>
    private void updateStatisticsPosition()
    {
        if(statistics != null)
        {
            var pos = Camera.main.WorldToScreenPoint(transform.position);
            var mappedValue = ui.RemapZoomValue(1, .2f);
            statistics.transform.position = new Vector3(pos.x + statisticsPositionOffsetX * mappedValue, pos.y + statisticsPositionOffsetY * mappedValue, pos.z);
            statistics.transform.localScale = new Vector3(mappedValue, mappedValue, 1);
        }
    }
}
