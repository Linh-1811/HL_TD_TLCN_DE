# XÂY DỰNG HỆ THỐNG PHẢN HỒI TIN NHẮN TỰ ĐỘNG SỬ DỤNG SPARK STREAMING, KAFKA, LSTM
Trong đề tài này, nhóm chúng em hướng tới việc giúp đỡ cho các hãng hàng không về khối lượng công việc như chăm sóc, phản hồi tin nhắn khách hàng, trải nghiệm của những người sử dụng dịch vụ các chuyến bay, hơn nữa bài toán phân tích cảm xúc được thực hiện dựa trên dữ liệu từ các phản hồi của khách hàng sẽ phần nào đó giúp được hãng hàng không hiểu rõ hơn về "tập khách hàng" và có thể nâng cấp, cải tiến các chất lượng dịch vụ để phù hợp với nhu cầu của khách hàng

#### thành viên nhóm
- Cao Hùng Lĩnh
- Đỗ Tiến Đạt


### Dataset
- Twitter Labelled Data (Training): https://www.crowdflower.com/data-for-everyone/
- Twitter Unlabelled Data (Training): Fetched customer tweets for selected 8 airlines
- Twitter Unlabelled Data (Testing): Fetching live tweets mentioning @DataMinersSfu

### Project Architecture
![image](https://user-images.githubusercontent.com/23083816/z6107865789875_914ef1847e7847e2d22bab39a705228c.png)

_All the initial commits were pushed in version-1 and after successfull validation it was merged with main branch_

### Các bước khởi động dự án

#### **1. Thử nghiệm trên Anaconda Command Prompt**
- Tải Anaconda
- Thiết lập Zookeeper:<br>
  Điều chỉnh zoopkeeper theo hệ thống của của từng máy. Trong trường hợp này, nhóm chúng em sẽ giữ nguyên các giá trị mặc định:
 
- Thiết lập kafka server<br>

 - Khởi động server:<br>
Truy cập Anaconda Command Prompt
 ```
Run docker compose up -d
conda activate env
conda activate env_consumer
 ```
- Khởi động Kafka producer:
```
python tele_producer.py
```
- Sử dụng Kafka Consumer để lắng nghe:
```
python tele_consumer.py
```


#### **2. Testing on CLI**
- Run twitter_cli.py
```
python3 twitter_cli.py
```
- Browse through the example tweets using Menu option - 1
- Test your example tweet using Menu option - 2
