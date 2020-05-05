using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// A UI box for showing attribute names and values.
/// </summary>
public class StatisticsBox : MonoBehaviour
{
    /// <summary>
    /// The font type to use when displaying text.
    /// </summary>
    [SerializeField]
    private Font font = null;

    /// <summary>
    /// The font size to use when displaying text.
    /// </summary>
    [SerializeField]
    private int fontSize = 14;

    /// <summary>
    /// Called on first frame. Sets up some variables.
    /// </summary>
    void Awake()
    {
        if (font == null)
        {
            font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        }
    }

    /// <summary>
    /// Adds a key-value entry into the UI. If one already exists,
    /// then the value will be updated.
    /// </summary>
    public void addEntry<T>(string name, T value)
    {
        var textTransform = gameObject.transform.Find(name);
        Text text;
        if (textTransform != null)
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

    /// <summary>
    /// If the given key exists, the entry will be removed from the UI.
    /// </summary>
    public void removeEntry(string name)
    {
        var textObject = gameObject.transform.Find(name).gameObject;
        if (textObject != null)
        {
            Destroy(textObject);
        }
    }

    /// <summary>
    /// Public method to destroy this game object.
    /// </summary>
    public void Destroy()
    {
        Destroy(gameObject);
    }
}
