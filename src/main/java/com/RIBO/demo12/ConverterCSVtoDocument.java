package com.RIBO.demo12;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import org.bson.Document;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

public class ConverterCSVtoDocument {
    private final File fileCSV;
    private Document documentBson;

    public ConverterCSVtoDocument(File fileCSV) {
        this.fileCSV = fileCSV;
    }

    public Document createDocument() throws IOException{
        List<Map<?, ?>> list;
        int cont = 0;
        list = readObjectsFromCsv();
        while (!list.isEmpty()) {
            Map<?,?> map = list.get(cont);

            documentBson.append("Organism Name", map.get(3));
            list.remove(cont);
            cont++;
        }
        return null;
    }

    public List<Map<?, ?>> readObjectsFromCsv() throws IOException {
        CsvSchema bootstrap = CsvSchema.emptySchema().withHeader();
        CsvMapper csvMapper = new CsvMapper();
        try (MappingIterator<Map<?, ?>> mappingIterator = csvMapper.readerFor(Map.class).with(bootstrap).readValues(fileCSV)) {
            return mappingIterator.readAll();
        }
    }
}
