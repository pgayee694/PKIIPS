using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Linq;
using SimpleJSON;

/// <summary>
/// Client used to communicate with Delphi.
/// </summary>
public class DelphiClient : MonoBehaviour
{
    /// <summary>
    /// Base URL of all of Delphi's endpoints.
    /// </summary>
    private static readonly string BASE_URL = Config.cfg["delphi client"]["base-url"].StringValue;

    /// <summary>
    /// Single instance of the client.
    /// </summary>
    private static DelphiClient _instance;

    /// <summary>
    /// Publicly accessible client instance.
    /// </summary>
    public static DelphiClient Instance
    {
        get
        {
            if (_instance == null)
                _instance = new GameObject("DelphiClient").AddComponent<DelphiClient>();
            return _instance;
        }
    }


    /// <summary>
    /// Prevents the client from being destroyed on scene change.
    /// </summary>
    void Awake()
    {
        if (_instance != null) Destroy(this);
        DontDestroyOnLoad(this);
    }


    /// <summary>
    /// Updates all of the fields for each of the nodes supplied.
    /// </summary>
    public void ToggleNodeStatus(Node node)
    {
        StartCoroutine(CallToggleStatus(node));
    }

    /// <summary>
    /// Updates all of the fields for each of the nodes supplied.
    /// </summary>
    public void UpdateNodes(Node[] nodes)
    {
        int[] nodeIds = nodes.Select(node => node.Id).ToArray();
        StartCoroutine(CallGetCounts(nodeIds, (response) => nodes.ToList().ForEach(node => node.PeopleCount = response[node.Id])));
        StartCoroutine(CallGetStatuses(nodeIds, (response) => nodes.ToList().ForEach(node => node.Status = response[node.Id])));
    }


    /// <summary>
    /// Helper method used to generate a list of parameters.
    /// </summary>
    private string GenerateParams(string key, int[] values)
    {
        return "?" + string.Join("&", values.Select(value => key + "=" + value).ToArray());
    }


    /// <summary>
    /// Gets the status of all of the nodes given in the list of ids.
    /// </summary>
    IEnumerator CallGetStatuses(int[] nodeIds, System.Action<JSONNode> callback)
    {
        UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-statuses" + GenerateParams("room_id", nodeIds));
        yield return www.SendWebRequest();

        if (www.isNetworkError || www.isHttpError)
        {
            Debug.LogError(www.error);
            yield break;
        }

        JSONNode response = JSON.Parse(www.downloadHandler.text);

        callback(response);
    }

    /// <summary>
    /// Gets the people count of all of the nodes given in the list of ids.
    /// </summary>
    IEnumerator CallGetCounts(int[] nodeIds, System.Action<JSONNode> callback)
    {
        UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-counts" + GenerateParams("room_id", nodeIds));
        yield return www.SendWebRequest();

        if (www.isNetworkError || www.isHttpError)
        {
            Debug.LogError(www.error);
            yield break;
        }

        JSONNode response = JSON.Parse(www.downloadHandler.text);

        callback(response);
    }

    /// <summary>
    /// Updates the status of the node associated with the given id.
    /// </summary>
    IEnumerator CallToggleStatus(Node node)
    {
        JSONObject requestData = new JSONObject();
        requestData.Add("enable", (!node.Status).ToString());

        UnityWebRequest www = UnityWebRequest.Put(BASE_URL + "/enable/" + node.Id, requestData.ToString());
        www.SetRequestHeader("Content-Type", "application/json");
        yield return www.SendWebRequest();

        if (www.isNetworkError || www.isHttpError)
        {
            Debug.LogError(www.error);
            yield break;
        }

        node.Status = !node.Status;
    }
}