<p>
This library makes working with kafka in python easy. It simplifies the producing of records. The producer class persists
fields so that the fields of a record can be retrieved in various places from within your code base.
</p>
<p>
The library that expands on the work of Confluent's kafka-python library to make an intuitive producer that simplifies coding. This producer acts as a Super Class that you can inherit all of your specific producers in your code. The implementation takes five lines of code
</p>

<ul>
  <li>Set the KAFKA_REGISTRY_LISTENER and KAFKA_BROKER_LISTENER (2 lines of code)</li>
  <li>from kp_fraydit.producers.producer import Producer</li>
  <li>prod = Producer('my-topic')</li>
  <li>prod.addValueArgs(myField1='test')</li>
</ul>

<p>
That is all that is needed to produce a record.
</p>
<p>
It utilizes Confluent's amazing Exact-Once Semantics(EOS) architecture. That assurance takes time, however. To speed up the library, all producer instances pool their records and then the records are parallel processed. This enhances the speed of the library while maintaining the EOS assurance. The sacrifice of this pooling loses the guarantee of order preservation. The library allows for individual producer instances to maintain a separate pool that ensures order. 
</p>

<p>
The producer handles JSON and Avro schema automatically. Nested schema (Avro only) is handled. That means you can have records within records and the producer class knows how to handle that.
</p>

<p>
You can discover what fields are available, which fields are required, optional fields, specify optional fields that you want to include on each write, all from within the attributes of the producer.
</p>

https://fraydit.com
