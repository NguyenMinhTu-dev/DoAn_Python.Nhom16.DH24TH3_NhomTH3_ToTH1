-- Tạo cơ sở dữ liệu nếu nó chưa tồn tại
CREATE DATABASE IF NOT EXISTS QLXEVALAIXE
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sử dụng cơ sở dữ liệu
USE QLXEVALAIXE;
Drop database qlxevalaixe;
CREATE TABLE IF NOT EXISTS `TaiKhoanQuanTri` (
  `id_quan_tri` INT NOT NULL AUTO_INCREMENT,
  `ten_dang_nhap` VARCHAR(50) NOT NULL UNIQUE,
  `mat_khau_hash` VARCHAR(255) NOT NULL COMMENT 'Luôn lưu mật khẩu đã được hash',
  `ho_ten` VARCHAR(100) NULL,
  `vai_tro` ENUM('admin', 'manager') NOT NULL DEFAULT 'manager',
  `ngay_tao` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_quan_tri`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `KhachHang` (
  `id_khach_hang` INT NOT NULL AUTO_INCREMENT,
  `ho_ten` VARCHAR(100) NOT NULL,
  `so_dien_thoai` VARCHAR(15) NOT NULL UNIQUE,
  `email` VARCHAR(100) NULL UNIQUE,
  `hang_thanh_vien` ENUM('Đồng', 'Bạc', 'VIP') NOT NULL DEFAULT 'Đồng',
  `ngay_tham_gia` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_khach_hang`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `TaiXe` (
  `ma_tai_xe` VARCHAR(10) NOT NULL UNIQUE COMMENT 'Mã tài xế (VD: TX001)',
  `ho_ten` VARCHAR(100) NOT NULL,
  `so_dien_thoai` VARCHAR(15) NOT NULL UNIQUE,
  `email` VARCHAR(100) NULL UNIQUE,
  `so_bang_lai` VARCHAR(20) NOT NULL,
  `hang_xe_lai` VARCHAR(50) NULL COMMENT 'Loại xe được phép lái',
  `danh_gia_trung_binh` DECIMAL(3, 2) NOT NULL DEFAULT 5.0,
  `trang_thai` ENUM('Hoạt động', 'Tạm ngưng', 'Chờ duyệt') NOT NULL DEFAULT 'Chờ duyệt',
  `ngay_tham_gia` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ma_tai_xe`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `PhuongTien` (
  `id_phuong_tien` INT NOT NULL AUTO_INCREMENT,
  `bien_so_xe` VARCHAR(15) NOT NULL UNIQUE,
  `loai_xe` VARCHAR(50) NOT NULL COMMENT 'VD: VinFast VF 8',
  `so_km_da_di` INT NOT NULL DEFAULT 0,
  `ngay_bao_tri_cuoi` DATE NULL,
  `trang_thai` ENUM('Hoạt động', 'Bảo trì', 'Ngừng hoạt động') NOT NULL DEFAULT 'Hoạt động',
  `ma_tai_xe_phu_trach` VARCHAR(10) NULL UNIQUE COMMENT 'Tài xế đang phụ trách',
  PRIMARY KEY (`id_phuong_tien`),
  INDEX `fk_PhuongTien_TaiXe_idx` (`ma_tai_xe_phu_trach` ASC) VISIBLE,
  CONSTRAINT `fk_PhuongTien_TaiXe`
    FOREIGN KEY (`ma_tai_xe_phu_trach`)
    REFERENCES `TaiXe` (`ma_tai_xe`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `ChuyenXe` (
  `id_chuyen_xe` INT NOT NULL AUTO_INCREMENT,
  `id_khach_hang` INT NOT NULL COMMENT 'Khóa ngoại từ KhachHang.id_khach_hang',
  `ma_tai_xe` VARCHAR(10) NOT NULL COMMENT 'Khóa ngoại từ TaiXe.ma_tai_xe',
  `bien_so_xe` VARCHAR(15) NOT NULL COMMENT 'Khóa ngoại từ PhuongTien.bien_so_xe',
  
  `diem_don` VARCHAR(255) NOT NULL,
  `diem_den` VARCHAR(255) NOT NULL,
  `so_km` DECIMAL(10, 2) NULL,
  
  `thoi_gian_dat_xe` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `thoi_gian_ket_thuc` TIMESTAMP NULL DEFAULT NULL COMMENT 'NULL nếu chưa kết thúc',
  
  `tong_tien` DECIMAL(12, 0) NOT NULL,
  `phuong_thuc_thanh_toan` ENUM('Tiền mặt', 'Chuyển khoản', 'Thẻ') NOT NULL DEFAULT 'Tiền mặt',
  `trang_thai_chuyen_xe` ENUM('Hoàn thành', 'Đã hủy', 'Đang diễn ra') NOT NULL DEFAULT 'Đang diễn ra',
  `danh_gia_chuyen_xe` INT NULL DEFAULT NULL COMMENT 'Từ 1-5 sao',
  
  PRIMARY KEY (`id_chuyen_xe`),
  
  INDEX `fk_ChuyenXe_KhachHang_idx` (`id_khach_hang` ASC) VISIBLE,
  INDEX `fk_ChuyenXe_TaiXe_idx` (`ma_tai_xe` ASC) VISIBLE,
  INDEX `fk_ChuyenXe_PhuongTien_idx` (`bien_so_xe` ASC) VISIBLE,
  
  CONSTRAINT `fk_ChuyenXe_KhachHang`
    FOREIGN KEY (`id_khach_hang`)
    REFERENCES `KhachHang` (`id_khach_hang`)
    ON DELETE NO ACTION  
    ON UPDATE CASCADE,
    
  CONSTRAINT `fk_ChuyenXe_TaiXe`
    FOREIGN KEY (`ma_tai_xe`)
    REFERENCES `TaiXe` (`ma_tai_xe`)
    ON DELETE NO ACTION  
    ON UPDATE CASCADE,
    
  CONSTRAINT `fk_ChuyenXe_PhuongTien`
    FOREIGN KEY (`bien_so_xe`)
    REFERENCES `PhuongTien` (`bien_so_xe`)
    ON DELETE NO ACTION  
    ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO `TaiKhoanQuanTri` (`ten_dang_nhap`, `mat_khau_hash`, `ho_ten`, `vai_tro`) 
VALUES ('admin', '202cb962ac59075b964b07152d234b70', 'Quản Trị Viên Chính', 'admin')
ON DUPLICATE KEY UPDATE mat_khau_hash='202cb962ac59075b964b07152d234b70';


INSERT INTO `TaiKhoanQuanTri` (`ten_dang_nhap`, `mat_khau_hash`, `ho_ten`, `vai_tro`) 
VALUES ('manager01', '202cb962ac59075b964b07152d234b70', 'Trần Văn Long', 'manager')
ON DUPLICATE KEY UPDATE ten_dang_nhap=ten_dang_nhap; 


INSERT INTO `TaiXe` (`ma_tai_xe`, `ho_ten`, `so_dien_thoai`, `email`, `so_bang_lai`, `hang_xe_lai`, `danh_gia_trung_binh`, `trang_thai`)
VALUES
('TX001', 'Nguyễn Văn An', '0901234567', 'nguyenvana@example.com', '123456789', 'Xe 4 Chỗ', 4.8, 'Hoạt động'),
('TX002', 'Trần Văn Bình', '0912345678', 'tranvanbinh@example.com', '234567890', 'Xe 7 Chỗ', 4.5, 'Hoạt động'),
('TX003', 'Lê Thị Cẩm', '0923456789', 'lethicam@example.com', '345678901', 'Xe 4 Chỗ', 4.2, 'Tạm ngưng')
ON DUPLICATE KEY UPDATE ma_tai_xe=ma_tai_xe;


INSERT INTO `TaiXe` (`ma_tai_xe`, `ho_ten`, `so_dien_thoai`, `email`, `so_bang_lai`, `hang_xe_lai`, `danh_gia_trung_binh`, `trang_thai`)
VALUES
('TX004', 'Phạm Hùng Dũng', '0934567890', 'phamhungdung@example.com', '456789012', 'Xe 7 Chỗ', 4.9, 'Hoạt động'),
('TX005', 'Võ Thị Thu Hà', '0945678901', 'vothithuha@example.com', '567890123', 'Xe 4 Chỗ', 4.7, 'Hoạt động'),
('TX006', 'Đặng Văn Lâm', '0956789012', 'dangvanlam@example.com', '678901234', 'Xe Bán Tải', 5.0, 'Chờ duyệt'),
('TX007', 'Bùi Hoàng Việt', '0967890123', 'buihoangviet@example.com', '789012345', 'Xe 4 Chỗ', 4.6, 'Hoạt động'),
('TX008', 'Ngô Thanh Vân', '0978901234', 'ngothanhvan@example.com', '890123456', 'Xe 7 Chỗ', 4.8, 'Tạm ngưng')
ON DUPLICATE KEY UPDATE ma_tai_xe=ma_tai_xe;

INSERT INTO `KhachHang` (`ho_ten`, `so_dien_thoai`, `email`, `hang_thanh_vien`)
VALUES
('Nguyễn Thị An', '0901111222', 'nt.an@example.com', 'VIP'),
('Trần Văn Bình', '0912222333', 'tv.binh@example.com', 'Bạc')
ON DUPLICATE KEY UPDATE ho_ten=VALUES(ho_ten);

INSERT INTO `KhachHang` (`ho_ten`, `so_dien_thoai`, `email`, `hang_thanh_vien`)
VALUES
('Phạm Văn Cường', '0987654321', 'pvc@example.com', 'VIP'),
('Lê Văn Sĩ', '0911223344', 'levansi@example.com', 'Bạc'),
('Mai Phương', '0922334455', 'maiphuong@example.com', 'Đồng'),
('Hồ Thị Hà', '0933445566', 'hothiha@example.com', 'Bạc'),
('Đàm Vĩnh Phúc', '0944556677', 'damvinhphuc@example.com', 'Đồng')
ON DUPLICATE KEY UPDATE ho_ten=VALUES(ho_ten);

select * from KhachHang;

INSERT INTO `PhuongTien` (`bien_so_xe`, `loai_xe`, `so_km_da_di`, `ngay_bao_tri_cuoi`, `trang_thai`, `ma_tai_xe_phu_trach`)
VALUES
('51F-123.45', 'VinFast VF 8', 120500, '2025-10-10', 'Hoạt động', 'TX001'),
('29A-987.65', 'VinFast VF e34', 85000, '2025-11-01', 'Hoạt động', 'TX002'),
('92A-456.78', 'VinFast VF 9', 150200, '2025-09-15', 'Bảo trì', 'TX003')
ON DUPLICATE KEY UPDATE bien_so_xe=VALUES(bien_so_xe);

INSERT INTO `PhuongTien` (`bien_so_xe`, `loai_xe`, `so_km_da_di`, `ngay_bao_tri_cuoi`, `trang_thai`, `ma_tai_xe_phu_trach`)
VALUES
('51G-456.78', 'VinFast VF 9', 75000, '2025-08-01', 'Hoạt động', 'TX004'),
('43A-111.22', 'Toyota Vios', 25000, '2025-10-30', 'Hoạt động', 'TX005'),
('65C-333.44', 'Ford Ranger', 180000, '2025-07-15', 'Hoạt động', 'TX006'),
('51H-555.66', 'VinFast VF e34', 15000, '2025-11-05', 'Hoạt động', 'TX007'),
('30E-777.88', 'Toyota Innova', 210000, '2025-06-20', 'Ngừng hoạt động', NULL) -- Xe chưa gán tài xế
ON DUPLICATE KEY UPDATE bien_so_xe=VALUES(bien_so_xe);


INSERT INTO `ChuyenXe` 
(`id_khach_hang`, `ma_tai_xe`, `bien_so_xe`, `diem_don`, `diem_den`, `so_km`, `thoi_gian_dat_xe`, `thoi_gian_ket_thuc`, `tong_tien`, `phuong_thuc_thanh_toan`, `trang_thai_chuyen_xe`, `danh_gia_chuyen_xe`)
VALUES
(1, 'TX001', '51F-123.45', '123 Nguyễn Huệ, Q.1', 'Sân bay Tân Sơn Nhất', 15.2, '2025-11-10 08:30:00', '2025-11-10 09:15:00', 180000, 'Thẻ', 'Hoàn thành', 5),
(2, 'TX002', '29A-987.65', 'Vincom Bà Triệu, Hà Nội', 'Hồ Gươm', 5.1, '2025-11-11 14:00:00', '2025-11-11 14:30:00', 75000, 'Tiền mặt', 'Hoàn thành', 4),
(3, 'TX004', '51G-456.78', 'Bệnh viện Chợ Rẫy', '256 Lê Lợi, Q.1', 10.0, '2025-11-12 10:00:00', '2025-11-12 10:45:00', 130000, 'Chuyển khoản', 'Hoàn thành', 5),
(4, 'TX005', '43A-111.22', 'Cầu Rồng, Đà Nẵng', 'Bãi biển Mỹ Khê', 3.5, '2025-11-13 19:00:00', '2025-11-13 19:20:00', 50000, 'Tiền mặt', 'Hoàn thành', 4),
(1, 'TX007', '51H-555.66', 'Landmark 81', 'Dinh Độc Lập', 8.2, '2025-11-14 11:00:00', '2025-11-14 11:35:00', 110000, 'Thẻ', 'Hoàn thành', 5),
(5, 'TX001', '51F-123.45', 'Đại học Bách Khoa TPHCM', 'Ký túc xá khu B', 22.0, '2025-11-15 08:00:00', NULL, 250000, 'Tiền mặt', 'Đang diễn ra', NULL),
(6, 'TX002', '29A-987.65', 'Ga Hà Nội', 'Sân bay Nội Bài', 35.0, '2025-11-15 09:15:00', NULL, 400000, 'Chuyển khoản', 'Đang diễn ra', NULL),
(2, 'TX005', '43A-111.22', 'Ngũ Hành Sơn', 'Hội An', 25.0, '2025-11-13 09:00:00', '2025-11-13 09:10:00', 300000, 'Tiền mặt', 'Đã hủy', NULL),
(7, 'TX004', '51G-456.78', 'Bến xe Miền Đông mới', 'Chung cư Vinhomes', 12.0, '2025-11-14 16:00:00', '2025-11-14 16:40:00', 160000, 'Tiền mặt', 'Hoàn thành', 3),
(3, 'TX007', '51H-555.66', 'Công viên phần mềm Quang Trung', 'Bitexco Tower', 18.5, '2025-11-15 10:00:00', NULL, 210000, 'Thẻ', 'Đang diễn ra', NULL)
ON DUPLICATE KEY UPDATE id_chuyen_xe=id_chuyen_xe;