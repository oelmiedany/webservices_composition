package com.service.jaxrs.whatson;

import java.io.IOException;
import com.sun.jersey.api.container.httpserver.HttpServerFactory;
import com.sun.net.httpserver.HttpServer;

public class WhatsOnRESTStartUp {

    public static void main(String[] args) {

        try {

            //code repurposed from labs to start the server
            HttpServer server = HttpServerFactory.create("http://localhost:9988/whatsonrest/");//server is hosted on port 9988
            server.start();
            System.out.println("PRESS ENTER TO STOP THE SERVER");//closes the server if any input is provided
            System.in.read();
            server.stop(0);

        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
