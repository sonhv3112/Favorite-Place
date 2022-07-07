# Địa điểm yêu thích

## Mục đích

Chương trình này được cài đặt nhằm quản lý các địa điểm yêu thích sử dụng Socket, giao thức **UDP**. Với các chức năng chính sau:
* Truy vấn danh sách địa điểm.
* Truy vấn thông tin 1 địa điểm.
* Cho phép tải về hình ảnh đại diện (hình nhỏ đại diện) từ server về client cho tất cả các thành viên trong danh bạ.
* Cho phép tải về các hình ảnh 1 địa điểm từ server về client khi truy vấn 1 địa điểm (hình ảnh lớn của địa điểm).
* Hỗ trợ nhiều client truy cập đồng thời đến server.
## Cấu trúc chương trình

Chương trình bao gồm 2 thư mục là client và server. 

* Thư mục client chứa file <span style="color:red">**client.py** </span>, folder <span style="color:red">**assets** </span>, folder <span style="color:red">**function** </span> và folder <span style="color:red">**gui** </span>.

    * File <span style="color:red">**client.py** </span> dùng để chạy chương trình, khi chạy file này giao diện sẽ hiện lên.

    * Folder <span style="color:red">**assets** </span> là ảnh của các button được sử dụng để xây dựng GUI.

    * Folder <span style="color:red">**function** </span> chứa file <span style="color:red">**function.py** </span> là tập tin chứa các hàm chức năng xử lý các tác vụ của client (gửi yêu cầu, nhận phản hồi).

    * Folder <span style="color:red">**gui** </span>  các file <span style="color:red">**body.py** </span>, <span style="color:red">**header.py** </span> và <span style="color:red">**main.py** </span> đảm nhiệm các nhiệm vụ sau:
        * File <span style="color:red">**main.py** </span>: Tập tin chính để tạo GUI.
        * File <span style="color:red">**header.py** </span>: Tập tin tạo phần header chứa logo và thanh tìm kiếm.
        * File <span style="color:red">**body.py** </span>: Tâp tin tạo phần body chứa các nội dung hiển thị trên GUI.
        
* Thư mục server chứa thư mục <span style="color:red">**database** </span> và file <span style="color:red">**server.py** </span> có các tác vụ:
    * Thư mục <span style="color:red">**database** </span> chứa file <span style="color:red">**place.json** </span> là tập tin cấu trúc để lưu cơ sở dữ liệu các địa điểm yêu thích và folder <span style="color:red">**image** </span> dùng để lưu các ảnh tương ứng của các địa điểm lưu ở tập tin json.
    * File <span style="color:red">**server.py** </span> là tập tin chứa các hàm chức năng xử lý các tác vụ của server (nhận yêu cầu, gửi phản hồi).

## Cách chạy chương trình
1. Môi trường lập trình: Python 3.10.0
2. Các gói cần tải về để chạy chương trình:
* <span style="color:green">**Numpy** </span> với cách tải tại đây [INSTALLING NUMPY](https://numpy.org/install/).
* <span style="color:green">**PIL** </span> với cách tải tại đây [INSTALLING PILLOW](https://blog.finxter.com/python-install-pil/).
* <span style="color:green">**cv2** </span> với cách tải tại đây [INSTALLING OPENCV](https://pypi.org/project/opencv-python/),
3. Cách chạy chương trình:
* Đầu tiên ta sẽ chạy file <span style="color:red">**server.py** </span> ở thư mục server.
    Cú pháp biên dịch: <code>**python server.py**</code>.
* Cuối cùng ta chạy file <span style="color:red">**client.py** </span> ở thư mục client. Sau bước này, giao diện sẽ hiện ra và ta sẽ dễ dàng thao tác truy vấn thông tin.
    Cú pháp biên dịch: <code>**python client.py**</code>.