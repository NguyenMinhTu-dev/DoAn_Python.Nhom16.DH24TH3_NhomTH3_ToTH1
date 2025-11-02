CREATE database QLXEVALAIXE;
USE QLXEVALAIXE;
CREATE TABLE IF NOT EXISTS `TaiKhoan` (
  `id_tai_khoan` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `so_dien_thoai` VARCHAR(15) NOT NULL UNIQUE,
  `mat_khau_hash` VARCHAR(255) NOT NULL,
  `vai_tro` ENUM('Khách hàng', 'Tài xế', 'Quản trị viên') NOT NULL,
  `ngay_tao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_tai_khoan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `KhachHang` (
  `id_khach_hang` INT NOT NULL AUTO_INCREMENT,
  `id_tai_khoan` INT NOT NULL UNIQUE,
  `ho_ten` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id_khach_hang`),
  FOREIGN KEY (`id_tai_khoan`) REFERENCES `TaiKhoan`(`id_tai_khoan`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `LoaiXe` (
  `id_loai_xe` INT NOT NULL AUTO_INCREMENT,
  `ten_loai_xe` VARCHAR(100) NOT NULL,
  `gia_mo_cua` DECIMAL(10, 2) NOT NULL,
  `gia_moi_km` DECIMAL(10, 2) NOT NULL,
  `mo_ta` TEXT NULL,
  PRIMARY KEY (`id_loai_xe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `TaiXe` (
  `id_tai_xe` INT NOT NULL AUTO_INCREMENT,
  `id_tai_khoan` INT NOT NULL UNIQUE,
  `ma_tai_xe` VARCHAR(20) NOT NULL UNIQUE,
  `ho_ten` VARCHAR(255) NOT NULL,
  `so_bang_lai` VARCHAR(50) NOT NULL UNIQUE,
  `danh_gia_trung_binh` DECIMAL(3, 2) NOT NULL DEFAULT 0.0,
  `trang_thai` ENUM('Hoạt động', 'Tạm ngưng', 'Chờ duyệt') NOT NULL DEFAULT 'Chờ duyệt',
  PRIMARY KEY (`id_tai_xe`),
  FOREIGN KEY (`id_tai_khoan`) REFERENCES `TaiKhoan`(`id_tai_khoan`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Xe` (
  `id_xe` INT NOT NULL AUTO_INCREMENT,
  `id_tai_xe` INT NOT NULL UNIQUE,
  `id_loai_xe` INT NOT NULL,
  `bien_so_xe` VARCHAR(20) NOT NULL UNIQUE,
  `mau_xe` VARCHAR(100) NULL,
  `mau_sac` VARCHAR(50) NULL,
  PRIMARY KEY (`id_xe`),
  FOREIGN KEY (`id_tai_xe`) REFERENCES `TaiXe`(`id_tai_xe`) ON DELETE CASCADE,
  FOREIGN KEY (`id_loai_xe`) REFERENCES `LoaiXe`(`id_loai_xe`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `DonDatXe` (
  `id_don_dat` INT NOT NULL AUTO_INCREMENT,
  `id_khach_hang` INT NOT NULL,
  `id_tai_xe` INT NULL,
  `id_loai_xe` INT NOT NULL,
  `diem_don` TEXT NOT NULL,
  `diem_den` TEXT NOT NULL,
  `trang_thai` ENUM('Đang tìm tài xế', 'Đã chấp nhận', 'Đang di chuyển', 'Hoàn thành', 'Đã hủy') NOT NULL,
  `gia_cuoc` DECIMAL(10, 2) NULL,
  `ngay_tao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `gio_don_khach` DATETIME NULL,
  `gio_tra_khach` DATETIME NULL,
  PRIMARY KEY (`id_don_dat`),
  FOREIGN KEY (`id_khach_hang`) REFERENCES `KhachHang`(`id_khach_hang`),
  FOREIGN KEY (`id_tai_xe`) REFERENCES `TaiXe`(`id_tai_xe`),
  FOREIGN KEY (`id_loai_xe`) REFERENCES `LoaiXe`(`id_loai_xe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `HoaDon` (
  `id_hoa_don` INT NOT NULL AUTO_INCREMENT,
  `id_don_dat` INT NOT NULL UNIQUE,
  `tong_tien` DECIMAL(10, 2) NOT NULL,
  `phuong_thuc_thanh_toan` ENUM('Tiền mặt', 'Thẻ', 'Ví điện tử') NOT NULL,
  `trang_thai_thanh_toan` ENUM('Chưa thanh toán', 'Đã thanh toán') NOT NULL DEFAULT 'Chưa thanh toán',
  `ngay_xuat_hoa_don` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_hoa_don`),
  FOREIGN KEY (`id_don_dat`) REFERENCES `DonDatXe`(`id_don_dat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `DanhGia` (
  `id_danh_gia` INT NOT NULL AUTO_INCREMENT,
  `id_don_dat` INT NOT NULL UNIQUE,
  `id_khach_hang` INT NOT NULL,
  `id_tai_xe` INT NOT NULL,
  `diem_danh_gia` INT NOT NULL,
  `binh_luan` TEXT NULL,
  `ngay_tao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_danh_gia`),
  FOREIGN KEY (`id_don_dat`) REFERENCES `DonDatXe`(`id_don_dat`),
  FOREIGN KEY (`id_khach_hang`) REFERENCES `KhachHang`(`id_khach_hang`),
  FOREIGN KEY (`id_tai_xe`) REFERENCES `TaiXe`(`id_tai_xe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- DỮ LIỆU MẪU (ĐÃ CẬP NHẬT THEO TAIKHOAN)
-- -----------------------------------------------------

-- Bảng LoaiXe
INSERT INTO `LoaiXe` (`ten_loai_xe`, `gia_mo_cua`, `gia_moi_km`, `mo_ta`) VALUES
('Xe 4 Chỗ', 15000.00, 11000.00, 'Xe 4 chỗ tiêu chuẩn (Sedan, Hatchback)'),
('Xe 7 Chỗ', 20000.00, 14000.00, 'Xe 7 chỗ rộng rãi (SUV, MPV)'),
('Xe máy', 7000.00, 5000.00, 'Xe máy 2 bánh');

-- Bảng TaiKhoan (Tạo tài khoản trước)
INSERT INTO `TaiKhoan` (`email`, `so_dien_thoai`, `mat_khau_hash`, `vai_tro`) VALUES
('an.nguyen@email.com', '0901112221', 'hash_pw_an123', 'Khách hàng'),
('binh.tran@email.com', '0901112222', 'hash_pw_binh456', 'Khách hàng'),
('cuong.le@email.com', '0901112223', 'hash_pw_cuong789', 'Khách hàng'),
('nguyenvanan@example.com', '0901234567', 'hash_pw_tx1', 'Tài xế'),
('tranvanbinh@example.com', '0912345678', 'hash_pw_tx2', 'Tài xế'),
('lethicam@example.com', '0923456789', 'hash_pw_tx3', 'Tài xế'),
('phamvandung@example.com', '0934567890', 'hash_pw_tx4', 'Tài xế'),
('hoangthiem@example.com', '0945678901', 'hash_pw_tx5', 'Tài xế');

-- Bảng KhachHang (Liên kết với id_tai_khoan 1, 2, 3)
INSERT INTO `KhachHang` (`id_tai_khoan`, `ho_ten`) VALUES
(1, 'Nguyễn Văn An'),
(2, 'Trần Thị Bình'),
(3, 'Lê Văn Cường');

-- Bảng TaiXe (Liên kết với id_tai_khoan 4, 5, 6, 7, 8)
INSERT INTO `TaiXe` (`id_tai_khoan`, `ma_tai_xe`, `ho_ten`, `so_bang_lai`, `danh_gia_trung_binh`, `trang_thai`) VALUES
(4, 'TX001', 'Nguyễn Văn An', 'B2_111111', 0.0, 'Hoạt động'),
(5, 'TX002', 'Trần Văn Bình', 'B2_222222', 0.0, 'Hoạt động'),
(6, 'TX003', 'Lê Thị Cẩm', 'B2_333333', 0.0, 'Tạm ngưng'),
(7, 'TX004', 'Phạm Văn Dũng', 'B2_444444', 0.0, 'Hoạt động'),
(8, 'TX005', 'Hoàng Thị Em', 'B2_555555', 0.0, 'Chờ duyệt');

-- Bảng Xe (id_tai_xe vẫn là 1-5 vì đó là AUTO_INCREMENT)
INSERT INTO `Xe` (`id_tai_xe`, `id_loai_xe`, `bien_so_xe`, `mau_xe`, `mau_sac`) VALUES
(1, 1, '51A-123.45', 'Toyota Vios', 'Trắng'),
(2, 2, '51B-234.56', 'Honda CRV', 'Đen'),
(3, 1, '51C-345.67', 'Mazda 3', 'Bạc'),
(4, 1, '51D-456.78', 'Kia Morning', 'Đỏ'),
(5, 1, '51E-567.89', 'Hyundai Accent', 'Trắng');

-- Bảng DonDatXe (id_khach_hang 1-3 và id_tai_xe 1-5 vẫn hợp lệ)
INSERT INTO `DonDatXe` (`id_khach_hang`, `id_tai_xe`, `id_loai_xe`, `diem_don`, `diem_den`, `trang_thai`, `gia_cuoc`, `ngay_tao`, `gio_don_khach`, `gio_tra_khach`) VALUES
(1, 1, 1, '123 Nguyễn Văn Cừ, P.1, Q.5', '456 Lê Lợi, Q.1', 'Hoàn thành', 150000.00, '2025-10-27 09:15:00', '2025-10-27 09:20:00', '2025-10-27 09:45:00'),
(2, 2, 2, '789 CMT8, P.10, Q.3', '101 Hai Bà Trưng, Q.1', 'Hoàn thành', 210000.00, '2025-10-27 10:30:00', '2025-10-27 10:35:00', '2025-10-27 11:05:00'),
(1, 4, 1, '111 Điện Biên Phủ, Q.Bình Thạnh', '222 Võ Văn Tần, Q.3', 'Hoàn thành', 120000.00, '2025-10-28 14:00:00', '2025-10-28 14:05:00', '2025-10-28 14:25:00'),
(3, 1, 1, '333 An Dương Vương, Q.5', '555 Sư Vạn Hạnh, Q.10', 'Đã hủy', NULL, '2025-10-28 15:00:00', NULL, NULL);

-- Bảng HoaDon (Giả định ID Đơn Đặt 1, 2, 3)
INSERT INTO `HoaDon` (`id_don_dat`, `tong_tien`, `phuong_thuc_thanh_toan`, `trang_thai_thanh_toan`) VALUES
(1, 150000.00, 'Thẻ', 'Đã thanh toán'),
(2, 210000.00, 'Ví điện tử', 'Đã thanh toán'),
(3, 120000.00, 'Tiền mặt', 'Đã thanh toán');

-- Bảng DanhGia (Giả định ID Đơn Đặt 1, 2, 3)
INSERT INTO `DanhGia` (`id_don_dat`, `id_khach_hang`, `id_tai_xe`, `diem_danh_gia`, `binh_luan`) VALUES
(1, 1, 1, 5, 'Tài xế thân thiện, xe sạch sẽ.'),
(2, 2, 2, 4, 'Xe 7 chỗ rộng rãi, nhưng tài xế chạy hơi ẩu.'),
(3, 1, 4, 5, 'Rất hài lòng!');

select * from KhachHang;
select * from Xe;