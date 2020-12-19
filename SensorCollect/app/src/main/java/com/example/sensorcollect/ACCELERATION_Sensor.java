package com.example.sensorcollect;

import android.annotation.SuppressLint;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.ArrayList;

import redis.clients.jedis.Jedis;

public class ACCELERATION_Sensor implements SensorEventListener {
    int pack_size = 32;
    int one_pack_size = 4;
    byte[] data = new byte[4 * pack_size * one_pack_size];
    ArrayList<byte[]> datas = new ArrayList<>();
    int pos = 0;
    InetAddress serverName;
    int PORT;
    Jedis jedis;
    int count = 0;
    private static final String TAG = "ACCELERATION_Sensor";

    public ACCELERATION_Sensor(InetAddress serverName, int port, String IPADDRESS){
        this.serverName = serverName;
        this.PORT = port;
        this.jedis = new Jedis(IPADDRESS, 6379, 5000);
    }

    @SuppressLint("SetTextI18n")
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        float X_lateral = 0, Y_longitudinal = 0, Z_vertical = 0;
        if (sensorEvent.sensor.getType() == Sensor.TYPE_LINEAR_ACCELERATION) {
            X_lateral = sensorEvent.values[0];
            Y_longitudinal = sensorEvent.values[1];
            Z_vertical = sensorEvent.values[2];
            float[] one_data = {count++, X_lateral, Y_longitudinal, Z_vertical};
            pushData2Server(one_data);
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }


    public void pushData2Server(float[] a) {

        for (float aa : a) {
            byte[] bytes = Utils.float2byte(aa);

            for (int i = pos, j = 0; j < 4; i++, j++) {
                data[i] = bytes[j];
            }
            pos += 4;
        }

        if (pos == data.length) {
            pos = 0;
            datas.add(data);
            new ConnectionThread().start();
        }
    }


    class ConnectionThread extends Thread {
//        byte[] msg;

        @Override
        public void run() {
            Log.d(TAG, "run: send");
////            msg = Arrays.copyOf(data, 8 * pack_size);
//            if (s == null) {
//                try {
//                    s = new DatagramSocket();
//                    dp = new DatagramPacket(data, data.length, serverName, PORT);
////                    soc = new Socket(IP_ADDRESS, PORT);
//                    //获取socket的输入输出流
////                    dos = new DataOutputStream(soc.getOutputStream());
//
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//            }
//            try {
////                System.out.println(data.length);
//                dp.setData(data);
//                s.send(dp);
////                dos.flush();
////                soc = null;
//            } catch (IOException e) {
//                e.printStackTrace();
//            }

            jedis.lpush("acc".getBytes(), data);
        }
    }
}
