using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class StatisticsBox : MonoBehaviour
{
    [SerializeField]
    private Font font = null;

    [SerializeField]
    private int fontSize = 14;

    void Awake()
    {
        if(font == null)
        {
            font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        }
    }

    public void addEntry<T>(string name, T value)
    {
        var textTransform = gameObject.transform.Find(name);
        Text text;
        if(textTransform != null)
        {
            text = textTransform.gameObject.GetComponent<Text>();
        }
        else
        {
            var textObject = new GameObject(name);
            textObject.transform.parent = gameObject.transform;

            text = textObject.AddComponent<Text>();
            text.font = font;
            text.fontSize = fontSize;
        }

        text.text = name + ": " + value.ToString();
    }

    public void removeEntry(string name)
    {
        var textObject = gameObject.transform.Find(name).gameObject;
        if(textObject != null)
        {
            Destroy(textObject);
        }
    }

    public void Destroy()
    {
        Destroy(gameObject);
    }
}
