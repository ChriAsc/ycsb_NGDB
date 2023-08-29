    
package site.ycsb.workloads;
import site.ycsb.DB;
import site.ycsb.Status;
import site.ycsb.Workload;
import site.ycsb.generator.UniformLongGenerator;
import java.util.HashMap;
import java.util.Arrays;
import java.util.Properties;
import site.ycsb.*;
import site.ycsb.ByteIterator;
import site.ycsb.StringByteIterator;
import site.ycsb.generator.*;
import site.ycsb.measurements.Measurements;

import java.io.IOException;
import java.util.*;

/**
 * Prova.
 */
public class CustomWorkload extends Workload {
  private NumberGenerator operationChooser;
  private NumberGenerator keyChooser;
  private NumberGenerator fieldValueLengthGenerator;

  @Override
  public void init(Properties properties) throws WorkloadException{
    operationChooser = new UniformLongGenerator(0, 99); // 0-99 for 100%
    keyChooser = new UniformLongGenerator(1, 10000); // 1-10000 keys
    fieldValueLengthGenerator = new UniformLongGenerator(10, 100); // Field value length

        // Additional initialization for the database connection or setup can go here
  }

  @Override
  public boolean doInsert(DB db, Object threadState) {
    String key = Integer.toString(keyChooser.nextValue().intValue());
    Map<String, ByteIterator> values = new HashMap<String, ByteIterator>();
    values.put("field1", generateRandomValue(fieldValueLengthGenerator.nextValue().intValue()));
    values.put("field2", generateRandomValue(fieldValueLengthGenerator.nextValue().intValue()));
    Status result = db.insert("table1", key, values);
    return result == Status.OK;
  }

  @Override
  public boolean doTransaction(DB db, Object threadState) {
    int operation = operationChooser.nextValue().intValue();
    String key = Integer.toString(keyChooser.nextValue().intValue());

    try {
      if (operation < 70) {
        // 70% read operation
        Map<String, ByteIterator> results = new HashMap<String, ByteIterator>();
        db.read("table1", key, null, results);
      } else if (operation < 90) {
        // 20% insert operation
        Map<String, ByteIterator> values = new HashMap<String, ByteIterator>();
        values.put("field1", generateRandomValue(fieldValueLengthGenerator.nextValue().intValue()));
        values.put("field2", generateRandomValue(fieldValueLengthGenerator.nextValue().intValue()));
        db.insert("table1", key, values);
      } else {
        // 10% update operation
        Map<String, ByteIterator> updateValues = new HashMap<String, ByteIterator>();
        updateValues.put("field1", generateRandomValue(fieldValueLengthGenerator.nextValue().intValue()));
        db.update("table1", key, updateValues);
      }
      return true;
    } catch (Exception e) {
      e.printStackTrace();
      return false;
    }
  }


  private ByteIterator generateRandomValue(int length) {
    // Generate a random alphanumeric string of given length
    // You might want to use a more sophisticated random data generator library
    // to create realistic data
    String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    StringBuilder sb = new StringBuilder(length);
    for (int i = 0; i < length; i++) {
      int index = (int) (Math.random() * characters.length());
      sb.append(characters.charAt(index));
    }
    ByteIterator res = new StringByteIterator(sb.toString());
    return res;
  }

}
