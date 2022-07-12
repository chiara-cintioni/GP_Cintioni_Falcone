package com.RIBO.demo12;


import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import org.json.JSONObject;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.mongodb.DBObject;
import com.mongodb.util.JSON;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import static org.springframework.util.SerializationUtils.serialize;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) throws IOException {



		SpringApplication.run(DemoApplication.class, args);

		// Creating a new logger, setting its level to SEVERE, creating a new client, a new database and a new collection.
		Logger mongoLogger = Logger.getLogger("org.mongodb.driver");
		mongoLogger.setLevel(Level.SEVERE);
		MongoClient client = new MongoClient("localhost");
		MongoDatabase db = client.getDatabase("databaseProvaDemo");

		MongoCollection<Document> demoDB = db.getCollection("DatiProfDaIntellij");

		File file = new File("C:-Users-Denise-Desktop-GroupProject-Documents-EnaEukaryota.txt");
		ENATree.getInstance().insertMany(file);










		/**

		File input = new File("C:\\Users\\Chiara\\OneDrive\\Desktop\\benchmark-results\\Archaea\\23S-structures.csv");
		File output = new File("C:\\Users\\Chiara\\OneDrive\\Desktop\\provaQuesto2.json");
		ConverterCSVToJson converterCSVToJson = new ConverterCSVToJson(input,output);
		 *
		 */
	}
}