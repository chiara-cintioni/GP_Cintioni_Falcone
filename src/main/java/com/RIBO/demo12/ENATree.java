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
            Node<String> root = new Node<>("Tassonomia ENA: ",10,0);
            ENATree = new ENATree(root);
        }
        return ENATree;
    }

    /**
     * The function takes a file as an argument, reads the file line by line, and inserts each line into the tree
     *
     * @param file the file that contains the data to be inserted
     */
    public void insertMany(File file) throws IOException {
        Scanner scanner = new Scanner(file);
        String name, s;
        int lvltree, rank;
        while(scanner.hasNext()){
            s = scanner.next();
            name = s.substring(4);
            lvltree = Integer.parseInt(s.substring(0,1));
            rank = Integer.parseInt(s.substring(2,3));
            Node<String> node1 = new Node<String>(name,rank,lvltree);
            recursiveTraceBack(node1);
        }
        scanner.close();
    }

    /**
     * The function takes a node as a parameter and checks if the node is a child of the current node. If it is, it adds
     * the node as a child of the current node and sets the current node to the node passed as a parameter. If it is not,
     * it sets the current node to the parent of the current node and calls the function again
     *
     * @param node1 the node that we want to add to the tree
     */
    private void recursiveTraceBack(Node<String> node1) {
        if(node.getLvlTree()+1 == node1.getLvlTree()){
            node.addChild(node1);
            node = node1;
        }else{
            node = node.getParent();
            recursiveTraceBack(node1);
        }
    }

    @Override
    public boolean isEmpty() {
        return super.isEmpty();
    }

    @Override
    public Node<String> getRoot() {
        return super.getRoot();
    }

    @Override
    public void setRoot(Node<String> root) {
        super.setRoot(root);
    }

    @Override
    public boolean exists(String key) {
        return super.exists(key);
    }

    @Override
    public int size() {
        return super.size();
    }

    @Override
    public int getNumberOfDescendants(Node<String> node) {
        return super.getNumberOfDescendants(node);
    }

    @Override
    public boolean find(Node<String> node, String keyNode) {
        return super.find(node, keyNode);
    }

    @Override
    public Node<String> findNode(Node<String> node, String keyNode) {
        return super.findNode(node, keyNode);
    }

    @Override
    public ArrayList<Node<String>> getPreOrderTraversal() {
        return super.getPreOrderTraversal();
    }

    @Override
    public ArrayList<Node<String>> getPostOrderTraversal() {
        return super.getPostOrderTraversal();
    }

    @Override
    public void buildPreOrder(Node<String> node, ArrayList<Node<String>> preOrder) {
        super.buildPreOrder(node, preOrder);
    }

    @Override
    public void buildPostOrder(Node<String> node, ArrayList<Node<String>> postOrder) {
        super.buildPostOrder(node, postOrder);
    }

    @Override
    public ArrayList<Node<String>> getLongestPathFromRootToAnyLeaf() {
        return super.getLongestPathFromRootToAnyLeaf();
    }

    @Override
    public int getHeight() {
        return super.getHeight();
    }

    @Override
    public ArrayList<ArrayList<Node<String>>> getPathsFromRootToAnyLeaf() {
        return super.getPathsFromRootToAnyLeaf();
    }

    @Override
    public void getPath(Node<String> node, ArrayList<Node<String>> currentPath, ArrayList<ArrayList<Node<String>>> paths) {
        super.getPath(node, currentPath, paths);
    }

    @Override
    public ArrayList<Node<String>> clone(ArrayList<Node<String>> list) {
        return super.clone(list);
    }
}
