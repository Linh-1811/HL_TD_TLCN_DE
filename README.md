# XÂY DỰNG HỆ THỐNG PHẢN HỒI TIN NHẮN TỰ ĐỘNG SỬ DỤNG SPARK STREAMING, KAFKA, LSTM
Trong đề tài này, nhóm chúng em hướng tới việc giúp đỡ cho các hãng hàng không về khối lượng công việc như chăm sóc, phản hồi tin nhắn khách hàng, trải nghiệm của những người sử dụng dịch vụ các chuyến bay, hơn nữa bài toán phân tích cảm xúc được thực hiện dựa trên dữ liệu từ các phản hồi của khách hàng sẽ phần nào đó giúp được hãng hàng không hiểu rõ hơn về "tập khách hàng" và có thể nâng cấp, cải tiến các chất lượng dịch vụ để phù hợp với nhu cầu của khách hàng

#### thành viên nhóm
- Cao Hùng Lĩnh
- Đỗ Tiến Đạt

### Kiến trúc hệ thống
![image](https://github.com/Linh-1811/HL_TD_TLCN_DE/blob/main/z6107865789875_914ef1847e7847e2d22bab39a705228c.jpg)


### Các bước khởi động dự án

#### ** Setup trên Anaconda Command Prompt**
- Tải Anaconda
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
