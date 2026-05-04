function muarandom(id) {
  swal({
    title: "Thông báo",
    text: "Bạn có chắc chắn muốn mua tài khoản Random này?",
    icon: "warning",
    buttons: {
      cancel: "Huỷ bỏ",
      confirm: {
        text: "Mua Ngay",
        closeModal: true,
        className: "btn btn-success"
      }
    },
    dangerMode: true
  }).then(function(confirm) {
    if (confirm) {
      $.ajax({
        url: '/pay_random', // link muốn gửi request
        type: 'post', // gửi đi bằng method
        Datatype: 'json',
        data: {
          id: id
        },
        success: function(data) {
          data = JSON.parse(data);
          if (data.status == "success") {
            swal({
              title: data.title,
              text: data.message,
              icon: "success",
            });
            setTimeout(function() {
              window.location.href = '/user/history-random';
            }, 2000);
          } else {
            swal({
              title: data.title,
              text: data.message,
              icon: "error",
            });
          }
        }
      });
    } else {
      swal({
        title: "Huỷ bỏ",
        text: "Bạn đã huỷ yêu cầu mua tài khoản Random.",
        icon: "info",
      });
    }
  });
}


function muanick(id) {
	swal({
    title: "Thông báo",
    text: "Bạn có chắc chắn muốn mua nick này?",
    icon: "warning",
    buttons: {
        confirm: "Đồng ý",
        cancel: "Huỷ bỏ",
    },
    dangerMode: true,
    closeModal: true,
}).then(function(confirm) {
    if(confirm) {
        $.ajax({
            url: '/pay_nick',
            type: 'post',
            Datatype: 'json',
            data: {
                id: id
            },
            success: function(data){
                data = JSON.parse(data);
                if(data.status== "success"){
                    swal({
                        title : data.title,
                        text: data.message,
                        icon: "success",
                    });
                    setTimeout(function(){
                        window.location.href = '/user/history-game';
                    }, 2000);
                } else {
                    swal({
                        title : data.title,
                        text: data.message,
                        icon: "error",
                    });
                }
            }
        });
    } else {
        return false;
    }
});

}