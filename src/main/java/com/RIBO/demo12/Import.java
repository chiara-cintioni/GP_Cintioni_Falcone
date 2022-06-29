package com.RIBO.demo12;

import org.json.CDL;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Objects;
import java.util.stream.Collectors;


    public class Import{
        public static void main(String[] args) {
             // Read csv data file and store it in a string
            InputStream is = Import.class.getResourceAsStream("C:\\Users\\Chiara\\OneDrive\\Desktop\\Archaea23S.csv");
            String csv = new BufferedReader(

                    new InputStreamReader(Objects.requireNonNull(is), StandardCharsets.UTF_8))
                    .lines()
                    .collect(Collectors.joining("\n"));

                try {
                    // Convert csv text to JSON string, and save it
                // to a data.json file.
                String json = CDL.toJSONArray(csv).toString(2);
                Files.write(Path.of("data.json"), json.getBytes());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

