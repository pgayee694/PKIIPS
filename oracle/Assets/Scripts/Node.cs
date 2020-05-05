﻿using UnityEngine;
using System.Collections;

/// <summary>
/// Script used to represent a node in our graph model.
/// </summary>
public abstract class Node : GraphComponent
{
    /// <summary>
    /// The default color of the node.
    /// </summary>
    public virtual Color NodeColor { get { return Color.white; } }

    /// <summary>
    /// The name of the people count attribute.
    /// </summary>
    public const string PeopleCountAttribute = "People Count";

    /// <summary>
    /// The name of the id attribute.
    /// </summary>
    public const string IdAttribute = "Id";

    /// <summary>
    /// The name of the status attribute.
    /// </summary>
    public const string StatusAttribute = "Status";

    /// <summary>
    /// The time in which it takes a double click to register.
    /// </summary>
    private const float Delay = .25f;

    /// <summary>
    /// Controls when clicks are counted. 
    /// </summary>
    private bool waitingOnClicks = false;

    /// <summary>
    /// The current number of clicks registered within the delay.
    /// </summary>
    private int clickCount = 0;

    /// <summary>
    /// The number of people in this node.
    /// </summary>
    private int peopleCount = 0;

    /// <summary>
    /// An ID for this node.
    /// </summary>
    private int id = 0;

    /// <summary>
    /// The status for this node.
    /// </summary>
    private bool status = false;

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
    /// Public attribute for the <code>status</code> member.
    /// Updates the UI entry when this value gets sets.
    /// <see cref="status"/>
    /// </summary>
    public bool Status
    {
        get { return status; }
        set
        {
            status = value;
            UpdateEntry(StatusAttribute, Status);

            if (this != null)
            {
                ParticleSystem ps = GetComponent<ParticleSystem>();
                var main = ps.main;
                main.startColor = Status ? NodeColor : Color.grey;
            }

        }
    }

    /// <summary>
    /// Used to keep track of the number of clicks within a certain wait period.
    /// </summary>
    private IEnumerator ClickCounter()
    {
        waitingOnClicks = true;
        yield return new WaitForSeconds(Delay);

        if (clickCount == 1)
        {
            ToggleStatisticsBox();
        }
        else
        {
            DelphiClient.Instance.ToggleNodeStatus(this);
        }

        waitingOnClicks = false;
        clickCount = 0;
    }

    /// <summary>
    /// Toggles the node status on a double click and StatisticsBox on a single click.
    /// </summary>
    protected override void OnMouseUp()
    {
        clickCount++;
        if (!waitingOnClicks)
        {
            StartCoroutine(ClickCounter());
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
        UpdateEntry(StatusAttribute, Status);
    }
}