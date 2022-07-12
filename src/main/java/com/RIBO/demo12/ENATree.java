package com.RIBO.demo12;

import org.springframework.data.mongodb.core.schema.MongoJsonSchema;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class ENATree extends Tree<String> {

    private static ENATree ENATree;
    private Node<String> node;

    private ENATree(Node<String> node) {
        super(node);
    }

    public static  ENATree getInstance(){
        if(ENATree == null){
            Node<String> root = new Node<>("Tassonomia ENA: ","");
            ENATree = new ENATree(root);
        }
        return ENATree;
    }

    public void insertMany(File file) throws IOException {
        Path path = file.toPath();
        List<String> list = Files.lines(path).toList();
        String name, lvltree, rank;
        for (String s : list) {
            name = s.substring(4);
            lvltree = s.substring(0,0);
            rank = s.substring(2,2);
            Node<String> node1 = new Node<String>(name,rank);
            node.addChild(node1);
            node = node1;
            System.out.println(name+ lvltree+rank);
        }
    }

}
