//+------------------------------------------------------------------+
//|                                                      ProjectName |
//|                                      Copyright 2018, CompanyName |
//|                                       http://www.companyname.net |
//+------------------------------------------------------------------+
#include <Zmq/Zmq.mqh>
datetime LastActiontime;

bool s;
bool e;
int start_bar;
int end_bar;
double start_close;
double end_close;
datetime start_time;
datetime end_time;

double previous_ask=0;
double previous_bid=0;
extern int period = 100;
bool order_opened = false;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int start()
  {

   bool has_position_on_chart = trades_on_symbol(Symbol());
   if(has_position_on_chart == false)
     {
      order_opened = false;
     }

   double close_price;
   close_price=iClose(Symbol(),0,1);
   double open_price;
   open_price=iOpen(Symbol(),0,1);

   double current_atr = iATR(NULL,0,21,0);


   double current_ma=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,0);
   double previous_ma1=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,1);
   double previous_ma2=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,2);
   double previous_ma3=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,3);
   double previous_ma4=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,4);
   double previous_ma5=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,5);
   double previous_ma6=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,6);
   double previous_ma7=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,7);
   double previous_ma8=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,8);
   double previous_ma9=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,9);
   double previous_ma10=iMA(Symbol(),0,period,0,MODE_EMA,PRICE_CLOSE,10);

   double current_close = iClose(NULL,0,0);
   double previous_close_1 = iClose(NULL,0,1);
   double previous_close_2 = iClose(NULL,0,2);
   double previous_close_3 = iClose(NULL,0,3);
   double previous_close_4 = iClose(NULL,0,4);
   double previous_close_5 = iClose(NULL,0,5);
   double previous_close_6 = iClose(NULL,0,6);
   double previous_close_7 = iClose(NULL,0,7);
   double previous_close_8 = iClose(NULL,0,8);
   double previous_close_9 = iClose(NULL,0,9);
   double previous_close_10 = iClose(NULL,0,10);
   double previous_close_11 = iClose(NULL,0,11);

   double current_open = iOpen(NULL,0,0);
   double previous_open_1 = iOpen(NULL,0,1);
   double previous_open_2 = iOpen(NULL,0,2);
   double previous_open_3 = iOpen(NULL,0,3);
   double previous_open_4 = iOpen(NULL,0,4);
   double previous_open_5 = iOpen(NULL,0,5);
   double previous_open_6 = iOpen(NULL,0,6);
   double previous_open_7 = iOpen(NULL,0,7);
   double previous_open_8 = iOpen(NULL,0,8);
   double previous_open_9 = iOpen(NULL,0,9);
   double previous_open_10 = iOpen(NULL,0,10);

   double current_high = iHigh(NULL,0,0);
   double previous_high_1 = iHigh(NULL,0,1);
   double previous_high_2 = iHigh(NULL,0,2);
   double previous_high_3 = iHigh(NULL,0,3);
   double previous_high_4 = iHigh(NULL,0,4);
   double previous_high_5 = iHigh(NULL,0,5);
   double previous_high_6 = iHigh(NULL,0,6);
   double previous_high_7 = iHigh(NULL,0,7);
   double previous_high_8 = iHigh(NULL,0,8);
   double previous_high_9 = iHigh(NULL,0,9);
   double previous_high_10 = iHigh(NULL,0,10);
   double previous_high_11 = iHigh(NULL,0,11);

   double current_low = iLow(NULL,0,0);
   double previous_low_1 = iLow(NULL,0,1);
   double previous_low_2 = iLow(NULL,0,2);
   double previous_low_3 = iLow(NULL,0,3);
   double previous_low_4 = iLow(NULL,0,4);
   double previous_low_5 = iLow(NULL,0,5);
   double previous_low_6 = iLow(NULL,0,6);
   double previous_low_7 = iLow(NULL,0,7);
   double previous_low_8 = iLow(NULL,0,8);
   double previous_low_9 = iLow(NULL,0,9);
   double previous_low_10 = iLow(NULL,0,10);
   double previous_low_11 = iLow(NULL,0,11);


   int result_1 = check_cross_over2(previous_high_1,previous_low_1,previous_high_2,previous_low_2,previous_ma1);
   int result_2 = check_cross_over2(previous_high_2,previous_low_2,previous_high_3,previous_low_3,previous_ma2);
   int result_3 = check_cross_over2(previous_high_3,previous_low_3,previous_high_4,previous_low_4,previous_ma3);
   int result_4 = check_cross_over2(previous_high_4,previous_low_4,previous_high_5,previous_low_5,previous_ma4);
   int result_5 = check_cross_over2(previous_high_5,previous_low_5,previous_high_6,previous_low_6,previous_ma5);
   int result_6 = check_cross_over2(previous_high_6,previous_low_6,previous_high_7,previous_low_7,previous_ma6);
   int result_7 = check_cross_over2(previous_high_7,previous_low_7,previous_high_8,previous_low_8,previous_ma7);
   int result_8 = check_cross_over2(previous_high_8,previous_low_8,previous_high_9,previous_low_9,previous_ma8);
   int result_9 = check_cross_over2(previous_high_9,previous_low_9,previous_high_10,previous_low_10,previous_ma9);
   int result_10 = check_cross_over2(previous_high_10,previous_low_10,previous_high_11,previous_low_11,previous_ma10);


   int current_result = check_cross_over2(current_high,current_low,previous_high_1,previous_low_1,current_ma);
   if(result_1==-1 && result_2==-1 && result_3==-1 && result_4==-1 && result_5==-1 && result_6==-1&& result_7==-1&& result_8==-1&& result_9==-1&& result_10==-1 &&  current_result==1)
     {

      string action = "";
      string sl = "";
      if(LastActiontime!=Time[0] && order_opened==false)
        {

         if(previous_high_1<previous_ma1)
           {
            
            OrderSend(Symbol(),OP_BUY,0.01,Ask,200,Ask-2*current_atr,0);
            sl = DoubleToStr(Ask-2*current_atr,5);
            action = "Buy|sl:" + sl;
            Print("!!!!!!!!!",action);
           }
         if(previous_low_1>previous_ma1)
           {
            
            OrderSend(Symbol(),OP_SELL,0.01,Bid,200,Bid+2*current_atr,0);
            sl = DoubleToStr(Bid+2*current_atr,5);
            action = "Sell|sl:" + sl;
            Print("!!!!!!!!!",action);
           }

         Context context("helloworld");
         Socket socket(context,ZMQ_REP);

         socket.bind("tcp://*:5555");
         ZmqMsg request;
         socket.recv(request);
         string str = Period();
         string var1=Symbol() + "|" + str + "mins | " + action + " " + TimeToStr(TimeCurrent(),TIME_DATE|TIME_SECONDS);
         ZmqMsg reply(var1);
         // Send reply back to client
         socket.send(reply);
         order_opened = true;



        }
      LastActiontime=Time[0];
     }

   return(0);
  }





//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int check_cross_over2(double high, double low,double p_high,double p_low, double ma)
  {
   if(high>=ma && low<=ma)
     {
      return 1;
     }

// tiaokong
   if(p_high>=ma && p_low>=ma && high<=ma && low<=ma)
     {
      return 0;
     }

// tiaokong
   if(p_high<=ma && p_low<=ma && high>=ma && low>=ma)
     {
      return 0;
     }

   return -1;
  }



//+------------------------------------------------------------------+



//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool trades_on_symbol(string symbol)
  {
   for(int i=OrdersTotal()-1; OrderSelect(i,SELECT_BY_POS); i--)
      if(OrderSymbol()==symbol && OrderType()<2)
         return true;
   return false;
  }


