using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

public class Node : MonoBehaviour
{
    private int peopleCount;
    private int id;

    public int PeopleCount
    {
        get { return peopleCount; }
        set
        {
            peopleCount = value;
            updatePeopleCountStatistics();
        }
    }

    public int Id
    {
        get { return id; }
        set
        {
            id = value;
            updateIdStatistics();
        }
    }

    [SerializeField]
    private StatisticsBox statisticsTemplate = null;

    [SerializeField]
    private float statisticsPositionOffsetX = 0;

    [SerializeField]
    private float statisticsPositionOffsetY = 0;

    private UIManager ui;

    private StatisticsBox statistics = null;
    
    void Start()
    {
        ui = GameObject.Find("EventSystem").GetComponent<UIManager>();
        Assert.IsNotNull(statisticsTemplate);
        Assert.IsNotNull(ui);
        PeopleCount = 0;
        Id = 0;
    }

    void Update()
    {
        updateStatisticsPosition();
    }

    void OnMouseUp()
    {
        if(statistics == null)
        {
            statistics = Instantiate<StatisticsBox>(statisticsTemplate);
            statistics.transform.SetParent(ui.getCanvas().gameObject.transform);
            updatePeopleCountStatistics();
            updateIdStatistics();

            updateStatisticsPosition();
        }
        else
        {
            Destroy(statistics.gameObject);
        }
    }

    void OnDestroy()
    {
        if(statistics != null)
        {
            Destroy(statistics.gameObject);
        }

        Destroy(gameObject);
    }

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

    private void updatePeopleCountStatistics()
    {
        if(statistics != null)
        {
            statistics.addEntry("People Count", PeopleCount);
        }
    }

    private void updateIdStatistics()
    {
        if(statistics != null)
        {
            statistics.addEntry("Room", Id);
        }
    }
}
