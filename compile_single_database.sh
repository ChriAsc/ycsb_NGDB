mvn -pl site.ycsb:mongodb-binding -am clean package -DskipTests -Dcheckstyle.skip
tar xfvz ./mongodb/target/ycsb-mongodb-binding-0.18.0-SNAPSHOT.tar.gz