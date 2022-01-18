import javax.ws.rs.core.MediaType;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.config.ClientConfig;
import com.sun.jersey.api.client.config.DefaultClientConfig;

public class WhatsOnClient {

    private static String getResponse(WebResource service) {
        return service.accept(MediaType.APPLICATION_JSON).get(String.class);
    }

    public static void main (String[] args)
    {
        ClientConfig config = new DefaultClientConfig();
        Client client = Client.create(config);
        WebResource service = client.resource("http://localhost:9988/whatsonrest/whatson/query");

        long startTime = System.currentTimeMillis();

        WebResource experiment = service.path("2021-11-15");
        System.out.println("Results: " + getResponse(experiment));

        long stopTime = System.currentTimeMillis();
        System.out.println("\nTime taken in milliseconds: "+ (stopTime-startTime));

    }

}



