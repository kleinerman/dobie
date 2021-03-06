![IMAGE ALT TEXT](docs/images_readme/dobie_header.png)


About
=====

Dobie is a reliable and high scalable access control system. It can fit any kind of organization and it can manage a big amount of doors and people.  Based on a client-server architecture, the system is composed of a central server and many autonomous controller boards. Each controller, managed by the central server, can control up to three doors, and more controllers can be added on-demand to the system to manage more of them. Thanks to a reliable and asynchronous communication protocol, the central server can set permissions on the controllers and controllers can report events to the server at any time. 
Flexible access managing, high detailed reports and real-time monitoring are some of the strong features of the system.



![IMAGE ALT TEXT](docs/images_readme/controller.png)


Features
========

Detailed reports
----------------

The dashboard has a user-friendly interface to query any kind of event captured by the controllers.
Smart filters can help you search events by date, time slot, organization, person, zone, door, and even direction.

![IMAGE ALT TEXT](docs/images_readme/filters_screen.png)

Detailed reports can be retrieved and also exported as csv files.
![IMAGE ALT TEXT](docs/images_readme/report_screen.png)


High scalability
----------------

Dobie allows you to control as little as one access to hundreds of them.
The deployment of controllers can grow according to demand in a simple and easy way without changing the design of your infrastructure.
Each controller can deal with three doors with RFID readers in the entrance and the exit. In addition, a REX button can be installed in each door.
Each time a controller is added to the system, three doors more will become available to control. Adding controllers to the system is very easy from the dashboard.

![IMAGE ALT TEXT](docs/images_readme/add_controller_popup.png)



Real-Time monitoring
--------------------

The dashboard allows you to capture events in real-time by the controllers such as door states, door openings, not allowed accesses, and more. Additionally, you can check the general health of the whole access system. The dashboard will alert you if any of the controllers fails or is not reachable anymore.

![IMAGE ALT TEXT](docs/images_readme/realtime_monitoring_screen.png)


Autorecovery from network 0utages
---------------------------------

When faced with network outages, the controller board can work without network and it has the ability to automatically restore the connection with the central server without manual intervention. It can also keep all activity logs and send them to the main server after restoring the connection.
In the same way, all pending configuration and accesses created in the dashboard, will be sent to the controller after the recovery.


Stand alone mode
----------------

For medium and small installations, up to 50 doors, the central server and user interface can run in one of the controllers acting as the master. There is no need to have a dedicated server for this.


Demo video
==========

[![IMAGE ALT TEXT](http://img.youtube.com/vi/SP9pfVvoSz0/0.jpg)](http://www.youtube.com/watch?v=SP9pfVvoSz0 "Dobie Control Access System")

