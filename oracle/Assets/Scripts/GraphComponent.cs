using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

/// <summary>
/// Script used to model a graph component that contain various
/// displayable attributes.
/// </summary>
public class GraphComponent : MonoBehaviour
{
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
    /// Updates an entry in the statistics box, if one exists.
    /// </summary>
    /// <param name="attributeName">The name of the attribute to show</param>
    /// <param name="attribute">The value of the attribute to show</param>
    public void UpdateEntry<T>(string attributeName, T attribute)
    {
        if(statistics != null)
        {
            statistics.addEntry(attributeName, attribute);
        }
    }

    /// <summary>
    /// Remove an entry in the statistics box, if that one exists.
    /// </summary>
    /// <param name="attributeName">The name of the attribute to remove</param>
    public void RemoveEntry(string attributeName)
    {
        if(statistics != null)
        {
            statistics.removeEntry(attributeName);
        }
    }
    
    /// <summary>
    /// Called on the first frame. Sets up certain variables.
    /// </summary>
    virtual protected void Start()
    {
        ui = GameObject.Find("EventSystem").GetComponent<UIManager>();
        Assert.IsNotNull(statisticsTemplate);
        Assert.IsNotNull(ui);
    }

    /// <summary>
    /// Called every frame.
    /// </summary>
    virtual protected void Update()
    {
        UpdateStatisticsPosition();
    }

    /// <summary>
    /// The currently instantiated <code>StatisticsBox</code>.
    /// </summary>
    virtual protected void OnMouseUp()
    {
        if(statistics == null)
        {
            statistics = CreateStatisticsBox();
            UpdateStatisticsValues();
            UpdateStatisticsPosition();
        }
        else
        {
            Destroy(statistics.gameObject);
        }
    }

    /// <summary>
    /// Updates the statistics box with all the up-to-date values.
    /// This method is meant to be overridden and is called after the statistics box
    /// has been created.
    /// </summary>
    virtual protected void UpdateStatisticsValues()
    {
    }

    /// <summary>
    /// Creates a statistics box game object from the given prefab.
    /// </summary>
    /// <returns>An empty statistics object set in the canvas.</returns>
    virtual protected StatisticsBox CreateStatisticsBox()
    {
        var statisticsBox = Instantiate<StatisticsBox>(statisticsTemplate);
        statisticsBox.transform.SetParent(ui.getCanvas().gameObject.transform);
        return statisticsBox;
    }

    /// <summary>
    /// Called when this game object is destroyed.
    /// Will also destroy its corresponding statistics box.
    /// </summary>
    private void OnDestroy()
    {
        if(statistics != null)
        {
            Destroy(statistics.gameObject);
        }

        Destroy(gameObject);
    }

    /// <summary>
    /// Moves the statistics box's position to the node, rather than just being stuck in
    /// the UI screen space.
    /// </summary>
    private void UpdateStatisticsPosition()
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
