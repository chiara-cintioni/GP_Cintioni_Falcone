package com.RIBO.demo12;


import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) throws FileNotFoundException {



		SpringApplication.run(DemoApplication.class, args);

		// Creating a new logger, setting its level to SEVERE, creating a new client, a new database and a new collection.
		Logger mongoLogger = Logger.getLogger("org.mongodb.driver");
		mongoLogger.setLevel(Level.SEVERE);
		MongoClient client = new MongoClient("localhost");
		MongoDatabase db = client.getDatabase("databaseProvaDemo");

		MongoCollection<Document> demoDB = db.getCollection("DemoDB");

		//db.createCollection("DemoDBDaIntellij");
		//MongoCollection<Document> collectionProva = db.getCollection("DemoDBDaIntellij");




		Document provaDemo = new Document()
				.append("Nome", "Secondo")
				.append ("Cognome", "Levi");
		demoDB.insertOne(provaDemo);

	}
}