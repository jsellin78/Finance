
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

        Bars BTCUSD_t6; //TimeFrame you want the prices in. All Currencies / Index / Commodoties & Energys supported

        Symbol gbpjpy;
        Symbol gbpusd;
        Symbol gbpnzd;
        Symbol cadjpy;
        Symbol us30;
        Symbol nas100;
        Symbol xtiusd;
        Symbol usdjpy;
        Symbol usdcad;
        Symbol eurusd;
        Symbol eurchf;
        Symbol euraud;
        Symbol eurgbp;
        Symbol eurjpy;
        Symbol eurcad;
        Symbol nzdusd;
        Symbol audnzd;
        Symbol audusd;
        Symbol xauusd;
        Symbol btcusd;
        Symbol ger40;
        Symbol jpn225;
        Symbol cn50;
        Symbol xngusd;
        Symbol gbpaud;
        Symbol eurnzd;
        Symbol audcad;
        Symbol nzdcad;
        Symbol uk100;
        Symbol xptusd;
        Symbol xpdusd;
        Symbol xaujpy;
        Symbol Sugar;
        Symbol Coffee;
        Symbol Cotton;
        Symbol Cocoa;
        Symbol Wheat;
        Symbol Soybeans;
        Symbol Lumber;
        Symbol Corn;
        Symbol VIX;
        Symbol RghRice;
        Symbol gbpcad;
        Symbol SpotBrent;
        Symbol SpotCrude;
        Symbol xagusd;
        Symbol xaueur;
        Symbol xauaud;
        Symbol xaugbp;
        Symbol xagaud;
        Symbol xauchf;
        Symbol Copper;
        Symbol NatGas;
        Symbol Gasoline;

        DateTime BTCUSD_LastOpenTime;

        protected override void OnStart()
        {
            //System.Diagnostics.Debugger.Launch();
            BTCUSD_t6 = MarketData.GetBars(TimeFrame.Tick, "BTCUSD");
            gbpjpy = Symbols.GetSymbol("GBPJPY");
            gbpusd = Symbols.GetSymbol("GBPUSD");
            gbpnzd = Symbols.GetSymbol("GBPNZD");
            us30 = Symbols.GetSymbol("US30");
            nas100 = Symbols.GetSymbol("NAS100");
            xtiusd = Symbols.GetSymbol("XTIUSD");
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
            xauusd = Symbols.GetSymbol("XAUUSD");
            btcusd = Symbols.GetSymbol("BTCUSD");
            ger40 = Symbols.GetSymbol("GER40");
            jpn225 = Symbols.GetSymbol("JPN225");
            cn50 = Symbols.GetSymbol("CN50");
            xngusd = Symbols.GetSymbol("XNGUSD");
            cadjpy = Symbols.GetSymbol("CADJPY");
            usdjpy = Symbols.GetSymbol("USDJPY");
            gbpaud = Symbols.GetSymbol("GBPAUD");
            eurnzd = Symbols.GetSymbol("EURNZD");
            audcad = Symbols.GetSymbol("AUDCAD");
            nzdcad = Symbols.GetSymbol("NZDCAD");
            uk100 = Symbols.GetSymbol("UK100");
            xpdusd = Symbols.GetSymbol("XPDUSD");
            xptusd = Symbols.GetSymbol("XPTUSD");
            xaujpy = Symbols.GetSymbol("XAUJPY");
            Sugar = Symbols.GetSymbol("Sugar");
            Coffee = Symbols.GetSymbol("Coffee");
            Cotton = Symbols.GetSymbol("Cotton");
            Cocoa = Symbols.GetSymbol("Cocoa");
            Wheat = Symbols.GetSymbol("Wheat");
            Soybeans = Symbols.GetSymbol("Soybeans");
            Lumber = Symbols.GetSymbol("Lumber");
            Corn = Symbols.GetSymbol("Corn");
            VIX = Symbols.GetSymbol("VIX");
            RghRice = Symbols.GetSymbol("RghRice");
            gbpcad = Symbols.GetSymbol("GBPCAD");
            SpotBrent = Symbols.GetSymbol("SpotBrent");
            SpotCrude = Symbols.GetSymbol("SpotCrude");
            Gasoline = Symbols.GetSymbol("Gasoline");
            xagusd = Symbols.GetSymbol("XAGUSD");
            xaueur = Symbols.GetSymbol("XAUEUR");
            xauaud = Symbols.GetSymbol("XAUAUD");
            xaugbp = Symbols.GetSymbol("XAUGBP");
            xagaud = Symbols.GetSymbol("XAGAUD");
            xaugbp = Symbols.GetSymbol("XAUGBP");
            xauchf = Symbols.GetSymbol("XAUCHF");
            Copper = Symbols.GetSymbol("Copper");
            NatGas = Symbols.GetSymbol("NatGas");

        }

        protected override void OnBar()
        {

        }

        private static readonly HttpClient client = new HttpClient();

        protected override void OnTick()
        {
            if (BTCUSD_t6.OpenTimes.LastValue != BTCUSD_LastOpenTime)
            {
                BTCUSD_LastOpenTime = BTCUSD_t6.OpenTimes.LastValue;
                Print("gbpjpy: {0} | GBPUSD: {1} | gbpnzd: {2} | us30: {3} | USTEC: {4} | ", gbpjpy.Bid, gbpusd.Bid, gbpnzd.Bid, us30.Bid, nas100.Bid);

                using (var client = new HttpClient())
                {
                    var endpoint = new Uri("http://192.168.1.204:9095/posts"); //Send Prices to your http Server
                    var newPost = new Post
                    {
                        Time = DateTime.Now.AddMinutes(-1).ToString("yyyy-MM-dd HH:mm"),
                         us30 = us30.Bid,
                        gbpjpy = gbpjpy.Bid,
                        gbpusd = gbpusd.Bid,
                        cadjpy = cadjpy.Bid,
                        usdjpy = usdjpy.Bid,
                        nas100 = nas100.Bid,
                        xtiusd = xtiusd.Bid,
                        gbpnzd = gbpnzd.Bid,
                        usdcad = usdcad.Bid,
                        eurusd = eurusd.Bid,
                        eurchf = eurchf.Bid,
                        euraud = euraud.Bid,
                        eurgbp = eurgbp.Bid,
                        eurjpy = eurjpy.Bid,
                        eurcad = eurcad.Bid,
                        nzdusd = nzdusd.Bid,
                        audnzd = audnzd.Bid,
                        audusd = audusd.Bid,
                        xauusd = xauusd.Bid,
                        btcusd = btcusd.Bid,
                        ger40 = ger40.Bid,
                        jpn225 = jpn225.Bid,
                        cn50 = cn50.Bid,
                        xngusd = xngusd.Bid,
                        sugar = Sugar.Bid,
                        gbpaud = gbpaud.Bid,
                        gbpcad = gbpcad.Bid,
                        eurnzd = eurnzd.Bid,
                        audcad = audcad.Bid,
                        nzdcad = nzdcad.Bid,
                        uk100 = uk100.Bid,
                        xpdusd = xpdusd.Bid,
                        xptusd = xptusd.Bid,
                        xaujpy = xaujpy.Bid,
                        coffee = Coffee.Bid,
                        cotton = Cotton.Bid,
                        cocoa = Cocoa.Bid,
                        wheat = Wheat.Bid,
                        soybeans = Soybeans.Bid,
                        lumber = Lumber.Bid,
                        corn = Corn.Bid,
                        vix = VIX.Bid,
                        rghrice = RghRice.Bid,
                        SpotBrent = SpotBrent.Bid,
                        SpotCrude = SpotCrude.Bid,
                        Gasoline = Gasoline.Bid,
                        NatGas = NatGas.Bid,
                        xagusd = xagusd.Bid,
                        xaueur = xaueur.Bid,
                        xaugbp = xaugbp.Bid,
                        xagaud = xagaud.Bid,
                        xauaud = xauaud.Bid,
                        Copper = Copper.Bid,
                        xauchf = xauchf.Bid
                    };
                    var newPostJson = JsonConvert.SerializeObject(newPost);
                    var payload = new StringContent(newPostJson, Encoding.UTF8, "application/json");
                    var result = client.PostAsync(endpoint, payload).Result.Content.ReadAsStringAsync().Result;
                }
            }
        }
    }

}

