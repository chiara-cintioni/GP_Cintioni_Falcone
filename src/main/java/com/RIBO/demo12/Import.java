package com.RIBO.demo12;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;


    public class Import{
        public static void main(String[] args) throws IOException {
            File input = new File("C:\\Users\\Chiara\\OneDrive\\Desktop\\prova.csv");
            File output = new File("C:\\Users\\Chiara\\OneDrive\\Desktop\\data.json");

            List<Map<?, ?>> data = readObjectsFromCsv(input);
            writeAsJson(data, output);
        }

        public static List<Map<?, ?>> readObjectsFromCsv(File file) throws IOException {
            CsvSchema bootstrap = CsvSchema.emptySchema().withHeader();
            CsvMapper csvMapper = new CsvMapper();
            try (MappingIterator<Map<?, ?>> mappingIterator = csvMapper.readerFor(Map.class).with(bootstrap).readValues(file)) {
                return mappingIterator.readAll();
            }
        }

        public static void writeAsJson(List<Map<?, ?>> data, File file) throws IOException {
            ObjectMapper mapper = new ObjectMapper();
            mapper.writeValue(file, data);
        }
        }


