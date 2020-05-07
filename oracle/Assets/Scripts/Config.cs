using UnityEngine;
using SharpConfig;
using System.IO;

public class Config
{
    /// <summary>
    /// Configuration file's location.
    /// </summary>
    private static readonly string CONFIG_FILE = "oracle_config.ini";

    /// <summary>
    /// Used to access all configuration settings.
    /// </summary>
    public static Configuration cfg;

    static Config()
    {
        if (!File.Exists(CONFIG_FILE))
        {
            Debug.Log("Setting up a default config since no file was found!");
            SetupDefaultConfig();
        }
        else
        {
            Debug.Log("Config file found!");
            cfg = Configuration.LoadFromFile(CONFIG_FILE);
        }
    }

    /// <summary>
    /// Applies the default configuration settings when no configuration file is found.
    /// </summary>
    private static void SetupDefaultConfig()
    {
        cfg = new Configuration();
        cfg["delphi client"]["base-url"].StringValue = "localhost:5000";
        cfg["delphi client"]["update-constraint-endpoint"].StringValue = "/update-constraint-data";
    }
}
