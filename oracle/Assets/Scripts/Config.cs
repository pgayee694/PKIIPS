using UnityEngine;
using SharpConfig;
using System.IO;

public class Config : MonoBehaviour
{
    /// <summary>
    /// Configuration file's location.
    /// </summary>
    private static readonly string CONFIG_FILE = "config.ini";

    /// <summary>
    /// Used to access all configuration settings.
    /// </summary>
    public static Configuration cfg;


    /// <summary>
    /// Called when this game object is created.
    /// </summary>
    void Start()
    {
        if (!File.Exists(CONFIG_FILE))
        {
            Debug.Log("Setting up a default config since no file was found!");
            SetupDefaultConfig();
        }
        else
        {
            cfg = Configuration.LoadFromFile(CONFIG_FILE);
        }
    }

    /// <summary>
    /// Applies the default configuration settings when no configuration file is found.
    /// </summary>
    private void SetupDefaultConfig()
    {
        cfg = new Configuration();
        cfg["delphi client"]["base-url"].StringValue = "localhost:5000";
    }
}
