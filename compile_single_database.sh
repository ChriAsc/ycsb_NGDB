mvn -pl site.ycsb:redis-binding -am clean package -DskipTests -Dcheckstyle.skip
tar xfvz ./redis/target/ycsb-redis-binding-0.18.0-SNAPSHOT.tar.gz