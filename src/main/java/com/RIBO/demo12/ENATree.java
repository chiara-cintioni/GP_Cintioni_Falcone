package com.RIBO.demo12;

import org.apache.logging.log4j.util.Strings;
import org.springframework.data.mongodb.core.schema.MongoJsonSchema;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Stream;

public class ENATree extends Tree<String> {

    private static ENATree ENATree;
    private Node<String> node;

    private ENATree(Node<String> node) {
        super(node);
        this.node = node;
    }

    public static  ENATree getInstance(){
        if(ENATree == null){
            Node<String> root = new Node<>("Tassonomia ENA: ",10);
            ENATree = new ENATree(root);
        }
        return ENATree;
    }

    public void insertMany(File file) throws IOException {
        Scanner scanner = new Scanner(file);
        String name, s;
        int lvltree, rank;
        while(scanner.hasNext()){
            s = scanner.next();
            name = s.substring(4);
            lvltree = Integer.parseInt(s.substring(0,1));
            rank = Integer.parseInt(s.substring(2,3));
            Node<String> node1 = new Node<String>(name,rank);
            node.addChild(node1);
            node = node1;
            System.out.println(name + lvltree + rank);
        }
        scanner.close();
    }

}
