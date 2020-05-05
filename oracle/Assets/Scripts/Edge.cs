using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

/// <summary>
/// Script used to model a edge in our graph model.
/// </summary>
public class Edge : GraphComponent
{
    /// <summary>
    /// The name of the people count attribute.
    /// </summary>
    public const string PeopleCountAttribute = "People Count";

    /// <summary>
    /// The name of the id attribute.
    /// </summary>
    public const string IdAttribute = "Id";

    /// <summary>
    /// The number of people in this node.
    /// </summary>
    private int peopleCount = 0;

    /// <summary>
    /// An ID for this node.
    /// </summary>
    private int id = 0;

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
            UpdateEntry(PeopleCountAttribute, peopleCount);
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
            UpdateEntry(IdAttribute, id);
        }
    }

    /// <summary>
    /// Updates the statistics box with all the up-to-date values.
    /// This method is meant to be overridden and is called after the statistics box
    /// has been created.
    /// </summary>
    protected override void UpdateStatisticsValues()
    {
        UpdateEntry(IdAttribute, Id);
        UpdateEntry(PeopleCountAttribute, PeopleCount);
    }
}
