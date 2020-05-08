using UnityEngine;

/// <summary>
/// Script used to model a room in our graph model.
/// </summary>
public class Room : GraphComponentStatus
{
    /// <summary>
    /// The name of the people count attribute.
    /// </summary>
    public const string PeopleCountAttribute = "People Count";

    /// <summary>
    /// The name of the id attribute.
    /// </summary>
    public override string IDAttribute { get {return "Room #"; } }

    /// <summary>
    /// The number of people in this node.
    /// </summary>
    private int peopleCount = 0;

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
    /// Updates the statistics box with all the up-to-date values.
    /// This method is meant to be overridden and is called after the statistics box
    /// has been created.
    /// </summary>
    protected override void UpdateStatisticsValues()
    {
        base.UpdateStatisticsValues();
        UpdateEntry(PeopleCountAttribute, PeopleCount);
    }
}
