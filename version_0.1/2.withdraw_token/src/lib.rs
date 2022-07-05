use scrypto::prelude::*;

blueprint! {
    struct TokenMachine {
        //0.DEFINE RESOURCE
        user_vault: Vault,
        price:Decimal
    }

    impl TokenMachine{

        //1.CREATE FUNCTION 
        pub fn instantiate_machine (price: Decimal) -> (ComponentAddress,Bucket){
            //1.1.DINAR RESOURCE
            let user_vault: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "Dinars")
                .metadata("symbol", "DNR")
                .initial_supply(100);

            //1.2.ADMIN BADGE
            let admin_badge = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "AdminBadge")
                .initial_supply(1);

            //1.3.AUTHENTICATE
            // let access_rule = AccessRules::new()
            //     .method("withdraw",rule!(require(admin_badge.resource_address())))
            //     .default(rule!(allow_all));

            //1.4 INSTANTIATE COMPONENT
            let componet = Self{
                user_vault: Vault ::with_bucket(user_vault),
                price:price
            }
            .instantiate();
            // .add_access_check(access_rule);

            //1.5.RETURN COMPONENT AND BADE
            (componet.globalize(),admin_badge)
        }


        //WITHDRAW 
        pub fn withdraw(&mut self) -> Bucket {
            info!("Withdrawing");
            self.user_vault.take(2)
        }

        //2.CHECK BALANCE
        pub fn check_balance(&mut self) -> Bucket{
            info!("My balance is: {}", self.user_vault.amount());
            self.user_vault.take(0)
        }


    }
}
