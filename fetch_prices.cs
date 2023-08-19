using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using cAlgo.API.Internals;
using cAlgo.API;
using WebSocketSharp;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.WEuropeStandardTime, AccessRights = AccessRights.FullAccess)]
    public class Testbot : Robot
    {
        [Parameter(DefaultValue = 0.0)]
        public double Parameter { get; set; }

        public class Post
        {
            public string Time { get; set; }
            public Dictionary<string, double> Prices { get; set; }
     
        }

        private WebSocket _webSocket;
        
        Bars BTCUSD_t1;

        private Symbol gbpjpy;
        private Symbol gbpusd;
        private Symbol gbpnzd;
        private Symbol cadjpy;
        private Symbol us30;
        private Symbol usdjpy;
        private Symbol usdcad;
        private Symbol eurusd;
        private Symbol eurchf;
        private Symbol euraud;
        private Symbol eurgbp;
        private Symbol eurjpy;
        private Symbol eurcad;
        private Symbol nzdusd;
        private Symbol audnzd;
        private Symbol audusd;
        private Symbol xauusd;
        private Symbol btcusd;
        private Symbol gbpaud;
        private Symbol eurnzd;
        private Symbol audcad;
        private Symbol nzdcad;
        private Symbol usdcnh;
        private Symbol xaujpy;
        private Symbol gbpcad;
        private Symbol XAGUSD;
        private Symbol xageur;
        private Symbol xaueur;
        private Symbol xauaud;
        private Symbol XAUGBP;
        private Symbol xagaud;
        private Symbol usdchf;
        private Symbol chfjpy;
        DateTime BTCUSD_LastOpenTime;

        protected override async void OnStart()
        {
            _webSocket = new WebSocket("ws://192.168.1.220:5995");
            _webSocket.OnMessage += WebSocket_OnMessage;
            _webSocket.OnOpen += WebSocket_OnOpen;
            _webSocket.OnError += WebSocket_OnError;
            _webSocket.OnClose += WebSocket_OnClose;
            _webSocket.Connect();
            BTCUSD_t1 = MarketData.GetBars(TimeFrame.Tick, "BTCUSD");
            gbpjpy = Symbols.GetSymbol("GBPJPY");
            gbpusd = Symbols.GetSymbol("GBPUSD");
            gbpnzd = Symbols.GetSymbol("GBPNZD");
            us30 = Symbols.GetSymbol("US30");
            usdjpy = Symbols.GetSymbol("USDJPY");
            usdcad = Symbols.GetSymbol("USDCAD");
            eurusd = Symbols.GetSymbol("EURUSD");
            eurchf = Symbols.GetSymbol("EURCHF");
            euraud = Symbols.GetSymbol("EURAUD");
            eurgbp = Symbols.GetSymbol("EURGBP");
            eurjpy = Symbols.GetSymbol("EURJPY");
            eurcad = Symbols.GetSymbol("EURCAD");
            nzdusd = Symbols.GetSymbol("NZDUSD");
            audnzd = Symbols.GetSymbol("AUDNZD");
            audusd = Symbols.GetSymbol("AUDUSD");
            cadjpy = Symbols.GetSymbol("CADJPY");
            gbpaud = Symbols.GetSymbol("GBPAUD");
            eurnzd = Symbols.GetSymbol("EURNZD");
            audcad = Symbols.GetSymbol("AUDCAD");
            nzdcad = Symbols.GetSymbol("NZDCAD");
            xaujpy = Symbols.GetSymbol("XAUJPY");
            xauusd = Symbols.GetSymbol("XAUUSD");
            gbpcad = Symbols.GetSymbol("GBPCAD");
            xageur = Symbols.GetSymbol("XAGEUR");
            xaueur = Symbols.GetSymbol("XAUEUR");
            xauaud = Symbols.GetSymbol("XAUAUD");
            xagaud = Symbols.GetSymbol("XAGAUD");
            usdcnh = Symbols.GetSymbol("USDCNH");
            XAUGBP = Symbols.GetSymbol("XAUGBP");
            XAGUSD = Symbols.GetSymbol("XAGUSD");
            btcusd = Symbols.GetSymbol("BTCUSD");
            chfjpy = Symbols.GetSymbol("CHFJPY");
            usdchf = Symbols.GetSymbol("USDCHF");
            _webSocket.Connect();

            await Task.CompletedTask;
        }
        private void WebSocket_OnOpen(object sender, EventArgs e)
{
    Print("WebSocket connection opened");

}

private void WebSocket_OnError(object sender, ErrorEventArgs e)
{
    Print("WebSocket error: {0}", e.Exception.Message);
}

private void WebSocket_OnClose(object sender, CloseEventArgs e)
{
    Print("WebSocket connection closed. Code: {0}, Reason: {1}", e.Code, e.Reason);
}


        private void WebSocket_OnMessage(object sender, MessageEventArgs e)
        {
            Print("Received: {0}", e.Data);
        }

        protected override void OnTick()
        {
            if (_webSocket.ReadyState == WebSocketState.Open)
            {
               if (BTCUSD_t1.OpenTimes.LastValue != BTCUSD_LastOpenTime)
               {
                BTCUSD_LastOpenTime = BTCUSD_t1.OpenTimes.LastValue;
                Print("gbpjpy: {0} | GBPUSD: {1} | gbpnzd: {2}", gbpjpy.Bid, gbpusd.Bid, gbpnzd.Bid);
                
                var newPost = new Post
                {
                  // Time = DateTime.Now.ToString("yyyy-MM-dd HH:mm"),
                   Prices = new Dictionary<string, double>
                {
                    { "us30", us30.Bid },
                    { "usdjpy", usdjpy.Bid },
                    { "usdcnh", usdcnh.Bid },
                    { "gbpjpy", gbpjpy.Bid },
                    { "gbpusd", gbpusd.Bid },
                    { "cadjpy", cadjpy.Bid },
                    { "gbpnzd", gbpnzd.Bid },
                    { "usdcad", usdcad.Bid },
                    { "eurusd", eurusd.Bid },
                    { "eurchf", eurchf.Bid },
                    { "euraud", euraud.Bid },
                    { "eurgbp", eurgbp.Bid },
                    { "eurjpy", eurjpy.Bid },
                    { "eurcad", eurcad.Bid },
                    { "nzdusd", nzdusd.Bid },
                    { "audnzd", audnzd.Bid },
                    { "audusd", audusd.Bid },
                    { "gbpaud", gbpaud.Bid },
                    { "gbpcad", gbpcad.Bid },
                    { "eurnzd", eurnzd.Bid },
                    { "audcad", audcad.Bid },
                    { "nzdcad", nzdcad.Bid },
                    { "xauusd", xauusd.Bid },
                    { "xagusd", XAGUSD.Bid },
                    { "xageur", xageur.Bid },
                    { "xaueur", xaueur.Bid },
                    { "xauaud", xauaud.Bid },
                    { "xaugbp", XAUGBP.Bid },
                    { "xagaud", xagaud.Bid },
                    { "btcusd", btcusd.Bid },
                    { "usdchf", usdchf.Bid },
                    { "chfjpy", chfjpy.Bid }
                }
               };

               var newPostJson = JsonConvert.SerializeObject(newPost);
               
               Print("Sending: {0}", newPostJson);  
                _webSocket.Send(newPostJson);
             }
         }
       }
        protected override void OnStop()
        {
            _webSocket.Close();
        }
    }
}
