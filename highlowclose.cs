using cAlgo.API.Internals;
using System;
using cAlgo.API;
using System.Net.Http;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Text;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.WEuropeStandardTime, AccessRights = AccessRights.FullAccess)]
    public class Testbot : Robot
    {
        [Parameter(DefaultValue = 0.0)]
        public double Parameter { get; set; }
        public object PrevClose { get; private set; }
        public object Open { get; private set; }
        public object High { get; private set; }
        public object Low { get; private set; }
        public object Close { get; private set; }

        Bars USDJPY_m15;

        DateTime USDJPY_LastOpenTime;

        protected override void OnStart()
        {
            //System.Diagnostics.Debugger.Launch();
            USDJPY_m15 = MarketData.GetBars(TimeFrame.Minute15, "EURUSD");
        }

        protected override void OnBar()
        {

        }

        private static readonly HttpClient client = new HttpClient();

        protected override async void OnTick()
        {   
            if (USDJPY_m15.OpenTimes.LastValue != USDJPY_LastOpenTime)
            {
                USDJPY_LastOpenTime = USDJPY_m15.OpenTimes.LastValue;
                Print(" PrevClose: {0} | Open: {1} | High: {2} | Low: {3} | Close: {4}", Bars.ClosePrices.Last(2), Bars.OpenPrices.Last(1), Bars.HighPrices.Last(1), Bars.LowPrices.Last(1), Bars.ClosePrices.Last(1));
                //var url = "http://192.168.1.204:8099/";
                using(var client = new HttpClient())
                {
                 var endpoint = new Uri("http://192.168.1.204:8071/posts");
                    var newPost = new Post()
                    {
                        Time = DateTime.Now.AddMinutes(45).ToString("yyyy-MM-dd HH:mm"),
                        Currency = "usdjpy",
                        PrevClose = Bars.ClosePrices.Last(2),
                        Close = Bars.ClosePrices.Last(1),
                        Open = Bars.OpenPrices.Last(1),
                        High = Bars.HighPrices.Last(1),
                        Low = Bars.LowPrices.Last(1)
                    };
                 var newPostJson = JsonConvert.SerializeObject(newPost);
                 var payload = new StringContent(newPostJson, Encoding.UTF8, "application/json");
                 var result = client.PostAsync(endpoint, payload).Result.Content.ReadAsStringAsync().Result;
                 //{"PrevClosePrice", string.Format("PrevClose: {0} | Open; {1} | High; {2} | Low; {3} | Close; {4}", Bars.ClosePrices.Last(2), Bars.OpenPrices.Last(1), Bars.HighPrices.Last(1), Bars.LowPrices.Last(1), Bars.ClosePrices.Last(1))},
                 //{"OpenPrice", Bars.OpenPrices.Last(1).ToString()},
                };
                //var res = await client.PostAsync(url, new FormUrlEncodedContent(data));
                //var content = await res.Content.ReadAsStringAsync();
                //Console.WriteLine(content);
                //record Person(string Name, string Occupation  );

                //name = ",Bars.ClosePrices.Last(2), Bars.OpenPrices.Last(1), Bars.HighPrices.Last(1), Bars.LowPrices.Last(1), Bars.ClosePrices.Last(1));"
            }
        }
    }

}
