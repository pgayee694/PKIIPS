using UnityEngine;
using System.Collections;
using UnityEngine.Assertions;

/// <summary>
/// Script used to represent a graph component that can
/// be enabled or disabled in our graph model.
/// </summary>
public class GraphComponentStatus : GraphComponent
{
    /// <summary>
    /// The default color of the object.
    /// </summary>
    public virtual Color ObjectColor { get { return Color.white; } }

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
    /// The status for this node.
    /// </summary>
    private bool status = false;

     /// <summary>
    /// The particle system for this node.
    /// </summary>
    private ParticleSystem ps;

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
            if(status != value)
            {
                status = value;
                UpdateEntry(StatusAttribute, Status);

                if (this != null)
                {
                    if(ps != null)
                    {
                        var main = ps.main;
                        main.startColor = Status ? ObjectColor : Color.grey;
                    }

                    if(!status && pathManager.CurrentPath != null)
                    {
                        pathManager.CurrentPath.Remove(Id);
                        pathManager.CurrentPath = pathManager.CurrentPath;
                    }
                }
            }
        }
    }

    protected override void Start()
    {
        base.Start();
        ps = GetComponent<ParticleSystem>();
        Status = true;
    }

    /// <summary>
    /// Updates the statistics box with all the up-to-date values.
    /// This method is meant to be overridden and is called after the statistics box
    /// has been created.
    /// </summary>
    protected override void UpdateStatisticsValues()
    {
        base.UpdateStatisticsValues();
        UpdateEntry(StatusAttribute, Status);
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
            delphiClient.ToggleNodeStatus(this);
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
}