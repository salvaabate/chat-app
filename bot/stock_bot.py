import pika
import requests


API = ('https://stooq.com/q/l/?s=', '&f=sd2t2ohlcv&h&e=csv')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='stock_bot_queue', durable=True)


def make_return_str(company, api_data):
    # This API returns a stock average
    stock_high = api_data.get('High')
    stock_open = api_data.get('Open')
    stock_close = api_data.get('Close')
    stock_low = api_data.get('Low')

    # Try calculating OHLC average
    try:
        so, sh, sl, sc = map(float,
                             [stock_open, stock_high, stock_low, stock_close])
        average = (so + sh + sl + sc) / 4

        # Convert to string, with 2 significant figures
        str_avg = str(round(average, 2))

        return '%s quote is $%s per share.' % (company, str_avg)
    except Exception:
        pass


def get_stock_info(stock_code):
    url = API[0] + stock_code + API[1]
    r = requests.get(url)
    return parse(r.text)


def parse(stock_text, separator=','):
    data = stock_text.split()
    keys = data[0].split(separator)

    return {k: v for k, v in zip(keys, data[1].split(separator))}


def on_request(ch, method, props, body):
    body = body.decode('utf-8')
    result = get_stock_info(body)
    response = make_return_str(body, result)
    if response is None:
        response = f'{body} is not a real stock code'

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='stock_bot_queue', on_message_callback=on_request)
channel.start_consuming()
