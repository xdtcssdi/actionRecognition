package com.example.sensorcollect;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {
    private SensorManager sm;
    private TextView mtextViewx, mtextViewy, mtextViewz;
    private static final String TAG = "MainActivity";
    String IP_ADDRESS = "";
    int PORT = 553;
    ACCELERATION_Sensor acceleration_sensor;
    Button ipbtn, ipstop;
    EditText ipet;
    InetAddress serverName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initUI();

        //创建一个SensorManager来获取系统的传感器服务
        sm = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        ipstop.setOnClickListener(v -> sm.unregisterListener(acceleration_sensor));

        ipbtn.setOnClickListener(v -> {
            IP_ADDRESS = ipet.getText().toString();
            if (!Utils.ipCheck(IP_ADDRESS)) {
                Toast.makeText(v.getContext(), "IP地址错误", Toast.LENGTH_SHORT).show();
            } else {

                try {
                    serverName = InetAddress.getByName(IP_ADDRESS);
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                }
                if (acceleration_sensor == null) {
                    acceleration_sensor = new ACCELERATION_Sensor(serverName, PORT , IP_ADDRESS);
                }
                //加速度传感器
                sm.registerListener(acceleration_sensor, sm.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION), SensorManager.SENSOR_DELAY_UI);
            }
        });

    }


    public void initUI() {
        ipbtn = findViewById(R.id.ipbtn);
        ipstop = findViewById(R.id.ipstop);
        ipet = findViewById(R.id.ipet);
        mtextViewx = findViewById(R.id.mtextViewx);
        mtextViewy = findViewById(R.id.mtextViewy);
        mtextViewz = findViewById(R.id.mtextViewz);
    }

    @Override
    protected void onDestroy() {
        sm.unregisterListener(acceleration_sensor);
        super.onDestroy();
    }
}

