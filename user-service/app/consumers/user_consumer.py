from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from app.models.user_model import User, UserUpdate
from app.crud.user_crud import add_new_user, get_all_users, get_user_by_id, delete_user_by_id, update_user_by_id
from app.deps import get_session


async def consume_messages(topic, bootstrap_servers):

    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-user-consumer-group",
        # auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW")
            print(f"Received message on topic {message.topic}")
            user_data = json.loads(message.value.decode())
            print("TYPE", (type(user_data)))
            print(f"User Data {user_data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_user = add_new_user(
                    user_data=User(**user_data), session=session)
                print("DB_INSERT_USER", db_insert_user)
                
                # Event EMIT In NEW TOPIC

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()