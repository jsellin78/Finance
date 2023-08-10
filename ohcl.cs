using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using cAlgo.API;
using cAlgo.API.Internals;
using Newtonsoft.Json;

namespace cAlgo.Robots
{
    public class Post
    {
        public string time { get; set; }
        public string Currency { get; set; }
        public double PrevClose { get; set; }
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Close { get; set; }
    }

    [Robot(TimeZone = TimeZones.EEuropeStandardTime, AccessRights = AccessRights.FullAccess)]
    public class Testbot : Robot
    {
         private readonly Dictionary<string, Bars> _currencyBars = new Dictionary<string, Bars>();
        

        private DateTime _lastPostTime;

        private static readonly HttpClient _httpClient = new HttpClient();

        protected override void OnStart()
        {
        _currencyBars.Add("gbpusd", MarketData.GetBars(TimeFrame.Minute15, "GBPUSD"));
        _currencyBars.Add("gbpjpy", MarketData.GetBars(TimeFrame.Minute15, "GBPJPY"));
        _currencyBars.Add("gbpnzd", MarketData.GetBars(TimeFrame.Minute15, "GBPNZD"));
        _currencyBars.Add("gbpaud", MarketData.GetBars(TimeFrame.Minute15, "GBPAUD"));
        _currencyBars.Add("gbpcad", MarketData.GetBars(TimeFrame.Minute15, "GBPCAD"));
        _currencyBars.Add("gbpchf", MarketData.GetBars(TimeFrame.Minute15, "GBPCHF"));
        _currencyBars.Add("usdjpy", MarketData.GetBars(TimeFrame.Minute15, "USDJPY"));
        _currencyBars.Add("usdcad", MarketData.GetBars(TimeFrame.Minute15, "USDCAD"));
        _currencyBars.Add("usdchf", MarketData.GetBars(TimeFrame.Minute15, "USDCHF"));
        _currencyBars.Add("nzdusd", MarketData.GetBars(TimeFrame.Minute15, "NZDUSD"));
        _currencyBars.Add("audusd", MarketData.GetBars(TimeFrame.Minute15, "AUDUSD"));
        _currencyBars.Add("usdsek", MarketData.GetBars(TimeFrame.Minute15, "USDSEK"));
        _currencyBars.Add("eurusd", MarketData.GetBars(TimeFrame.Minute15, "EURUSD"));
        _currencyBars.Add("eurchf", MarketData.GetBars(TimeFrame.Minute15, "EURCHF"));
        _currencyBars.Add("eurcad", MarketData.GetBars(TimeFrame.Minute15, "EURCAD"));
        _currencyBars.Add("euraud", MarketData.GetBars(TimeFrame.Minute15, "EURAUD"));
        _currencyBars.Add("cadjpy", MarketData.GetBars(TimeFrame.Minute15, "CADJPY"));
            // Add additional currency pairs as needed
        }

        protected override void OnBar()
        {
            // Do any additional processing on each bar, if needed
        }

        protected override void OnTick()
        {
        
                    
            // Check if it's been at least 15 minutes since the last post
            if ((DateTime.Now - _lastPostTime).TotalMinutes >= 240)
            {
                // Record the current time as the last post time
                _lastPostTime = DateTime.Now;

                // Create a list of Post objects for each currency pair
                var posts = new List<Post>();
                foreach (var kvp in _currencyBars)
                {
                var currency = kvp.Key;
                var bars = kvp.Value;
                var openTimes = bars.OpenTimes;
                var lastOpenTime = openTimes.LastValue;
                var prevClose = bars.ClosePrices.Last(2);
                var open = bars.OpenPrices.Last(1);
                var high = bars.HighPrices.Last(1);
                var low = bars.LowPrices.Last(1);
                var close = bars.ClosePrices.Last(1);

                    var post = new Post
                    {
                        time = DateTime.Now.ToString("yyyy-MM-dd HH:mm"),
                        Currency = currency,
                        PrevClose = prevClose,
                        Open = open,
                        High = high,
                        Low = low,
                        Close = close
                    };

                    posts.Add(post);
                }

                // Convert the list of Post objects to JSON and send the data to the server
                var json = JsonConvert.SerializeObject(posts);
                var content = new StringContent(json, Encoding.UTF8, "application/json");
                var result = _httpClient.PostAsync(new Uri("http://192.168.1.186:5059/15min"), content).Result;
                var resultContent = result.Content.ReadAsStringAsync().Result;
            }
        }
    }
}
