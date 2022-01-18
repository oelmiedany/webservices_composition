package com.service.jaxrs.whatson;

//sql
import org.codehaus.jettison.json.JSONArray;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;

import java.io.*;
import java.sql.*;
import java.util.*;

//Jersey
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.DELETE;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.Consumes;
import javax.ws.rs.core.MediaType;

@Path("/whatson")
public class WhatsOnREST {

    private Connection database = null;

    //database methods

    private static Connection getConnection() throws SQLException
    {
        //connects to my jdbc database

        String drivers = "com.mysql.jdbc.Driver";
        System.setProperty("jdbc.drivers", drivers);

        String url = "jdbc:mysql://csdbdev/sc19oem_comp3211";
        String user = "sc19oem";
        String password = "password";

        //returns a connection to the jdbc database
        return DriverManager.getConnection(url, user, password);
    }

    //adds data to the database
    private static void addData(Connection database, String title, String director, String initialDate, String finalDate) throws SQLException
    {
        int currentID=0;

        Statement createStatement = database.createStatement();
        ResultSet results = createStatement.executeQuery("SELECT MAX(ID) FROM FilmDirectory");//identifies the largest ID number
        results.next();
        currentID= results.getInt(1);
        currentID++;//results in the new film ID number being larger than the previous IDs and as such unique

        PreparedStatement prepStatement = database.prepareStatement("INSERT INTO FilmDirectory VALUES(?,?,?,?,?)");

        //all the different variables are inputted to complete the database entry
        prepStatement.setInt(1, currentID);
        prepStatement.setString(2, title);
        prepStatement.setString(3, director);
        prepStatement.setString(4, initialDate);
        prepStatement.setString(5, finalDate);
        prepStatement.executeUpdate();

        prepStatement.close();

    }

    //deletes a record
    private static void removeData(Connection database, String title) throws SQLException
    {
        Statement createStatement = database.createStatement();
        createStatement.executeUpdate("DELETE FROM FilmDirectory WHERE title='"+title+"'");//deletes films with the inputted title
    }

    //retrieves all films that are playing in cinemas between two dates
    private static ArrayList<String> query(Connection database, String date)throws SQLException
    {
        ArrayList resultList= new ArrayList<String>();//stores all results in a list
        Statement createStatement = database.createStatement();
        ResultSet results = createStatement.executeQuery("SELECT * FROM FilmDirectory WHERE '"+date+"' between initialDate and finalDate");//finds all films within the inputted dates

        while(results.next())//loops through all results
        {
            resultList.add(results.getString("title"));//every film title is followed by the film's director
            resultList.add(results.getString("director"));
        }
        return resultList;
    }

    //prints database, used when debugging the REST method
    private static String printDatabase(Connection database) throws SQLException
    {
        //outputs all records within the database
        Statement createStatement = database.createStatement();
        ResultSet results = createStatement.executeQuery("SELECT * FROM FilmDirectory");
        String stringResults="";

        while (results.next()) {
            stringResults=stringResults+" "+results.getString("ID")+" "+results.getString("title")+" "+results.getString("initialDate")+" "+results.getString("finalDate")+"\n";
        }

        return stringResults;
    }

    //REST methods

    //queries the database and returns the results
    //determines what films are in cinemas on the date inputted
    @GET
    @Path("/query/{date}")
    @Produces(MediaType.APPLICATION_JSON)
    public String queryJSON(@PathParam("date") String date)throws IOException, SQLException, JSONException
    {
        database = getConnection();

        ArrayList results=query(database,date);//stores the results from the query method above
        JSONArray response=new JSONArray();

        for (int i=0; i<results.size();i=i+2)
        {
            JSONObject temp=new JSONObject();
            temp.put("title",results.get(i));
            temp.put("director",results.get(i+1));
            response.put(temp);//the results are systematically turned into JSON objects and stored within a JSON Array
        }

        database.close();

        return response.toString();//The JSON Array is converted to a string to be returned
    }

    @GET
    @Path("/printall")
    @Produces(MediaType.TEXT_PLAIN)
    public String printall()throws IOException, SQLException
    {
        database = getConnection();

        String response=printDatabase(database);//outputs database as a String

        database.close();

        return response;
    }

    //allows a user to add new films into the database using the POST operation
    @POST
    @Path("/add/{title}/{director}/{initialDate}/{finalDate}")
    @Consumes(MediaType.TEXT_PLAIN)
    public void addResource(@PathParam("title") String title, @PathParam("director") String director, @PathParam("initialDate") String initialDate, @PathParam("finalDate") String finalDate)throws IOException, SQLException
    {
        database = getConnection();

        addData(database,title,director,initialDate,finalDate);//extracts all details form the URI

        database.close();
    }

    //allows the user to modify the database and delete a film through the DELETE operation
    @DELETE
    @Path("/remove/{title}")
    @Consumes(MediaType.TEXT_PLAIN)
    public void deleteResource(@PathParam("title") String title)throws IOException, SQLException
    {
        database = getConnection();

        removeData(database,title);//uses the title inputted by the user

        database.close();
    }
}