import javax.ws.rs.core.MediaType;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.config.ClientConfig;
import com.sun.jersey.api.client.config.DefaultClientConfig;

public class Service2Client {

    private static String getResponse(WebResource service) {
        return service.accept(MediaType.APPLICATION_JSON).get(String.class);
    }

    public static void main (String[] args)
    {
        ClientConfig config = new DefaultClientConfig();
        Client client = Client.create(config);
        WebResource service = client.resource("http://127.0.0.1:4500/by-director");

        long startTime = System.currentTimeMillis();

        WebResource experiment = service.path("EDGAR WRIGHT");
        System.out.println("Results: " + getResponse(experiment));

        long stopTime = System.currentTimeMillis();
        System.out.println("\nTime taken in milliseconds: "+ (stopTime-startTime));

    }
}



