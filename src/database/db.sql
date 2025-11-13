-- Tạo cơ sở dữ liệu nếu nó chưa tồn tại
CREATE DATABASE QLXEVALAIXE
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sử dụng cơ sở dữ liệu
USE QLXEVALAIXE;

-- -----------------------------------------------------
-- Bảng: TaiKhoanQuanTri (Users)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TaiKhoanQuanTri` (
  `id_quan_tri` INT NOT NULL AUTO_INCREMENT,
  `ten_dang_nhap` VARCHAR(50) NOT NULL UNIQUE,
  `mat_khau_hash` VARCHAR(255) NOT NULL COMMENT 'Luôn lưu mật khẩu đã được hash',
  `ho_ten` VARCHAR(100) NULL,
  `vai_tro` ENUM('admin', 'manager') NOT NULL DEFAULT 'manager',
  `ngay_tao` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_quan_tri`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Bảng: KhachHang (Customers)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `KhachHang` (
  `id_khach_hang` INT NOT NULL AUTO_INCREMENT,
  `ho_ten` VARCHAR(100) NOT NULL,
  `so_dien_thoai` VARCHAR(15) NOT NULL UNIQUE,
  `email` VARCHAR(100) NULL UNIQUE,
  `hang_thanh_vien` ENUM('Đồng', 'Bạc', 'VIP') NOT NULL DEFAULT 'Đồng',
  `ngay_tham_gia` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_khach_hang`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Bảng: TaiXe (Drivers)
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Bảng: PhuongTien (Vehicles)
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- (Bảng ChuyenDi đã được xóa)
-- -----------------------------------------------------


-- -----------------------------------------------------
-- Thêm Dữ Liệu Mẫu
-- -----------------------------------------------------

-- 1. Tài khoản Admin (Mật khẩu là 'admin123' - hash SHA2-256)
INSERT INTO `TaiKhoanQuanTri` (`ten_dang_nhap`, `mat_khau_hash`, `ho_ten`, `vai_tro`) 
VALUES ('admin', '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', 'Quản Trị Viên', 'admin')
ON DUPLICATE KEY UPDATE id_quan_tri=id_quan_tri;

-- 2. Dữ liệu Lái Xe
INSERT INTO `TaiXe` (`ma_tai_xe`, `ho_ten`, `so_dien_thoai`, `email`, `so_bang_lai`, `hang_xe_lai`, `danh_gia_trung_binh`, `trang_thai`)
VALUES
('TX001', 'Nguyễn Văn An', '0901234567', 'nguyenvana@example.com', '123456789', 'Xe 4 Chỗ', 4.8, 'Hoạt động'),
('TX002', 'Trần Văn Bình', '0912345678', 'tranvanbinh@example.com', '234567890', 'Xe 7 Chỗ', 4.5, 'Hoạt động'),
('TX003', 'Lê Thị Cẩm', '0923456789', 'lethicam@example.com', '345678901', 'Xe 4 Chỗ', 4.2, 'Tạm ngưng')
ON DUPLICATE KEY UPDATE ma_tai_xe=ma_tai_xe;

-- 3. Dữ liệu Khách Hàng
INSERT INTO `KhachHang` (`id_khach_hang`, `ho_ten`, `so_dien_thoai`, `email`, `hang_thanh_vien`)
VALUES
(1, 'Nguyễn Thị An', '0901111222', 'nt.an@example.com', 'VIP'),
(2, 'Trần Văn Bình', '0912222333', 'tv.binh@example.com', 'Bạc')
ON DUPLICATE KEY UPDATE id_khach_hang=id_khach_hang;

-- 4. Dữ liệu Phương Tiện
INSERT INTO `PhuongTien` (`id_phuong_tien`, `bien_so_xe`, `loai_xe`, `so_km_da_di`, `ngay_bao_tri_cuoi`, `trang_thai`, `ma_tai_xe_phu_trach`)
VALUES
(1, '51F-123.45', 'VinFast VF 8', 120500, '2025-10-10', 'Hoạt động', 'TX001'),
(2, '29A-987.65', 'VinFast VF e34', 85000, '2025-11-01', 'Hoạt động', 'TX002'),
(3, '92A-456.78', 'VinFast VF 9', 150200, '2025-09-15', 'Bảo trì', 'TX003')
ON DUPLICATE KEY UPDATE id_phuong_tien=id_phuong_tien;
select * from taixe
-- (Dữ liệu mẫu ChuyenDi đã được xóa)